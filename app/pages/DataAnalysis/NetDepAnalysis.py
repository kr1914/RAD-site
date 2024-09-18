import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import cv2 as cv
import numpy as np
import tools.tool as tool
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
import io
from scapy.all import rdpcap
from scapy.all import PcapReader
import time
import matplotlib.font_manager as fm

# 한글 폰트 설정
def set_korean_font():
    plt.rcParams['font.family'] = 'AppleGothic'  # Windows의 경우
    plt.rcParams['axes.unicode_minus'] = False  # 축의 마이너스 폰트 깨짐 방지

set_korean_font()

# 바이너리 형식으로 pcap 파일을 받아서 처리하는 경우
def process_pcap(binary_data, start_ip=None, start_port=None):
    result = {}
    with io.BytesIO(binary_data) as f:
        packets = PcapReader(f)

        max_packet = 100
        for i, packet in enumerate(packets):
            try:
                #print(f"Packet {i+1}: {packet.summary()}")
                #print(f"packet ;: {packet.show(dump=True)}")
                if max_packet < i:
                   break
                #TCP 통신만 처리
                if not packet.haslayer('IP') or not packet.haslayer('TCP'):
                    print(f"packet skip : {packet.show(dump=True)}")
                    continue
                
                #IP계층 / TCP 계층 정보
                ip_layer = packet.getlayer('IP')
                tcp_layer = packet.getlayer('TCP')
                
                if start_ip is not None and start_ip != '' and ip_layer.src != start_ip:
                    print(f"start_ip is None")
                    continue
                
                if start_port is not None and start_port.strip() != '' and tcp_layer.sport != int(start_port):
                    continue
                
                
                ip_port = f"{packet.getlayer('IP').src}:{packet.sport}"
                
                if result.get(ip_port) is None:
                    result[ip_port] = []
                    
                # IP와 TCP 계층 정보 추출

                # TCP 데이터 길이 계산 (IP 전체 길이 - IP 헤더 길이 - TCP 헤더 길이)
                ip_total_length = ip_layer.len  # IP 패킷 전체 길이
                ip_header_length = ip_layer.ihl * 4  # IP 헤더 길이 (ihl는 4바이트 단위)
                tcp_header_length = tcp_layer.dataofs * 4  # TCP 헤더 길이 (dataofs는 4바이트 단위)
                tcp_payload_length = ip_total_length - ip_header_length - tcp_header_length  # 전송된 데이터 길이
                

                # 딕셔너리로 변환할 패킷 정보 매핑
                packet_info = {
                    "Packet Number": i+1,
                    "Ethernet": {
                        "src": packet.src if hasattr(packet, 'src') else None,
                        "dst": packet.dst if hasattr(packet, 'dst') else None,
                        "type": packet.type if hasattr(packet, 'type') else None,
                    },
                    "IP": {
                        "src": packet.getlayer('IP').src if packet.haslayer('IP') else None,
                        "dst": packet.getlayer('IP').dst if packet.haslayer('IP') else None,
                        "ttl": packet.getlayer('IP').ttl if packet.haslayer('IP') else None,
                        "flags": packet.getlayer('IP').flags if packet.haslayer('IP') else None,
                    },
                    "TCP": {
                        "sport": packet.sport if packet.haslayer('TCP') else None,
                        "dport": packet.dport if packet.haslayer('TCP') else None,
                        "seq": packet.seq if packet.haslayer('TCP') else None,
                        "ack": packet.ack if packet.haslayer('TCP') else None,
                        "flags": packet.flags if packet.haslayer('TCP') else None,
                        "payload_length" : tcp_payload_length
                    }
                }
                
                result[ip_port].append(packet_info)
                
            except Exception as e:
                print(e)
                
        # PcapReader는 반드시 close()로 종료해야 함
        packets.close()

    return result

# 그래프 생성 함수
def make_graph_old(data, place_holder=None):
    # 그래프 생성
    G = nx.DiGraph()  # 방향성 있는 그래프 생성

    # 데이터에서 노드 및 엣지 추가
    center_node = list(data.keys())[0]  # 중앙 노드 (예: "192.168.219.162:49594")
    sub_nodes = data[center_node]  # 하위 노드 (예: "121.189.48.20:49594")

    # 중앙 노드 추가
    G.add_node(center_node)
    

    for sub_node_key, sub_node_value in sub_nodes.items():
        G.add_node(sub_node_key)
        G.add_edge(center_node, sub_node_key)

    # 레이아웃 설정
    pos = nx.spring_layout(G, k=0.7)
    
    # 애니메이션을 위한 초기 설정
    fig, ax = plt.subplots(figsize=(10, 8))
    
    def update(num):
        # TOTAL_PAYLOAD 값을 실시간으로 증가
        for sub_node_key in sub_nodes.keys():
            sub_nodes[sub_node_key]["TOTAL_PAYLOAD"] += 1000  # 임의로 payload 증가
        
        # 노드 크기 설정 (중앙 노드는 고정 크기, 하위 노드는 payload에 비례)
        node_sizes = [
            3000 if node == center_node else min(sub_nodes[node]["TOTAL_PAYLOAD"], 10000) 
            for node in G.nodes()
        ]
        
        # 이전 그래프 클리어
        ax.clear()
        
        # 그래프 다시 그리기
        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray", arrows=True, ax=ax)

        # 축 설정
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title("Network Graph - 각 노드별 PAYLOAD 양에 비례한 크기")
        ax.axis('off')

    # FuncAnimation으로 애니메이션 생성
    ani = FuncAnimation(fig, update, frames=10, interval=500, repeat=True)

    # Streamlit에 애니메이션을 표시 (한 프레임씩 업데이트)
    for _ in range(10):
        place_holder.pyplot(fig)
        time.sleep(0.5)  # 0.5초마다 업데이트

# 그래프 생성 함수
def make_graph(data, place_holder=None):
    # 그래프 생성
    G = nx.DiGraph()  # 방향성 있는 그래프 생성

    # 데이터에서 노드 및 엣지 추가
    center_node = list(data.keys())[0]  # 중앙 노드 (예: "192.168.219.162:49594")
    sub_nodes = data[center_node]  # 하위 노드 (예: "121.189.48.20:49594")

    # 중앙 노드 및 엣지 추가
    G.add_node(center_node)
    for sub_node_key, sub_node_value in sub_nodes.items():
        G.add_node(sub_node_key)
        G.add_edge(center_node, sub_node_key)
        
    # 노드 크기 설정 (애니메이션에서 업데이트될 값)
    node_sizes = [10 if node == center_node else min(30, sub_nodes[node]["TOTAL_PAYLOAD"]) if sub_nodes[node]["TOTAL_PAYLOAD"] > 5 else 5 for node in G.nodes()]
    
    # 노드 색상 설정
    node_colors = [0 if node == center_node else 1 for node in G.nodes()]
    
    max_node_size = max(node_sizes)  # 최대 노드 크기
    scaling_factor = max_node_size  # 노드 크기를 고려한 거리 조정
    
    # 네트워크 레이아웃 설정 (노드 크기에 비례한 거리 설정)
    # k 값을 크게 하여 노드 간 거리를 멀리 설정 (엣지 길이 조정)
    pos = nx.spring_layout(G, k=1.5, iterations=50, scale=1)
    #pos = nx.spring_layout(G, k=1.5 * scaling_factor)  # k 값을 노드 크기에 비례하여 조정

    # Plotly 그래프 데이터 초기화
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # For line break between edges
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    # 센터 노드가 없을 경우를 방지하고 센터 노드 크기를 설정
    #node_sizes = [500 if node == center_node else sub_nodes.get(node, {}).get("TOTAL_PAYLOAD", 30) for node in G.nodes()]
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=node_sizes,  # 초기 노드 크기 설정
            color=node_colors,  # 초기 색상 설정
            colorbar=dict(
                thickness=15,
                title='Node Size (PAYLOAD)',
                xanchor='left',
                titleside='right'
            ),
            line_width=2
        )
    )

    # 노드의 hover 정보 추가
    node_text = []
    for node in G.nodes():
        if node != center_node:
            node_text.append(f"Node {node}: PAYLOAD={sub_nodes[node]['TOTAL_PAYLOAD']}")
        else:
            node_text.append("Center Node")
    node_trace.text = node_text

    # Plotly 그래프 만들기
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Network Graph - PAYLOAD 기반 노드 크기',
                        titlefont_size=16,
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        annotations=[dict(
                            text="각 노드의 PAYLOAD 양에 비례한 크기",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002
                        )],
                        xaxis=dict(showgrid=False, zeroline=False, range=[-5, 5]),  # X축 패딩 추가
                        yaxis=dict(showgrid=False, zeroline=False, range=[-5, 5]),
                        )
                   )
    return fig

st.header("네트워크 패킷 분석(.pcap)")
# value = streamlit_image_coordinates("https://plantuml.com/imgw/img-e890b0fb49cf18a254ed383fa4710f81.png")
# st.write(value)
st.write("네트워크 구성 분석")
st.write("패킷중에 입력된 IP, PORT에서 출발한 패킷의 도착지 IP:PORT를 그래프로 표현한다.")

start_ip = st.text_input(label="발신IP", value="10.50.140.27")
start_port = st.text_input(label="발신PORT", value="8970", placeholder="8888")

uploaded_file = st.file_uploader("Choose a .pcap file")


#그래프 플레이스 홀더
graph_placeholder = st.empty()

if uploaded_file is not None:
    try:
        # Read the uploaded file
        bytes_data = uploaded_file.getvalue()
    

        # pcap 데이터를 출발지 ip_port 기준으로 딕셔너리 타입으로 저장
        packets_info = process_pcap(bytes_data, start_ip=start_ip, start_port=start_port)
        
        display_info = {}
        
        # 패킷 개수를 측정하는 부분
        #for key in packets_info.keys():
        #    display_info[key] = len(packets_info[key])
          
        #패킷의 도착지별로 분류  
        for key in packets_info.keys():
            packets = packets_info[key]
            for i, packet in enumerate(packets):
                if display_info.get(key) is None:
                    display_info[key] = {}
                dst_ip = packet['IP']["dst"]
                dst_port = packet['TCP']["dport"]
                payload_length = packet['TCP']["payload_length"]
                dst_info = f"{dst_ip}:{dst_port}"
                
                if display_info[key].get(dst_info) is None:
                    display_info[key][dst_info] = {
                        "IP" : dst_ip,
                        "PORT" : dst_port,
                        "TOTAL_PAYLOAD" : 0
                    }
                    
                display_info[key][dst_info]["TOTAL_PAYLOAD"] += payload_length
            
        
        fig = make_graph(display_info, place_holder=graph_placeholder)
        
        if (start_ip is None or start_ip.strip() == '') and (start_port is None or start_port.strip() == '') :
            #print(f"display_info print :: {display_info}")
            st.write(display_info)
        else : 
            graph_placeholder.plotly_chart(fig)
            #st.pyplot(plt)
        
        
        
        
    except Exception as e:
        st.error(f"bytes_data : {len(bytes_data)}")
        st.error(f"display_info: {display_info}")
        st.error(f"Error: {e}")
        




