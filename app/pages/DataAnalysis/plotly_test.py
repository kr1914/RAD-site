import streamlit as st
import networkx as nx
import plotly.graph_objects as go

# Streamlit 애플리케이션 제목
st.title("Network Graph with Hover Events")

# 네트워크 그래프 생성
G = nx.Graph()

# 노드 및 엣지 추가
G.add_node(1, label="Node 1", value=500)
G.add_node(2, label="Node 2", value=300)
G.add_node(3, label="Node 3", value=100)
G.add_edge(1, 2)
G.add_edge(2, 3)

# 네트워크 레이아웃 설정
pos = nx.spring_layout(G)

# Plotly 그래프 준비
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)  # For line break
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

# 엣지 그리기
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines')

# 노드 그리기
node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=[G.nodes[node]['value'] / 10 for node in G.nodes()],  # 노드 크기 비례
        color=[G.nodes[node]['value'] for node in G.nodes()],
        colorbar=dict(
            thickness=15,
            title='Node Value',
            xanchor='left',
            titleside='right'
        ),
        line_width=2)
)

# 노드의 hover 정보 추가
node_text = []
for node in G.nodes():
    node_text.append(f"Node {node}: Value={G.nodes[node]['value']}")
node_trace.text = node_text

# Plotly 그래프 만들기
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Network Graph with Hover',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=40),
                    annotations=[dict(
                        text="Hover over the nodes to see details",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002
                    )],
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False))
               )

# Streamlit에서 Plotly 그래프 출력
st.plotly_chart(fig)
