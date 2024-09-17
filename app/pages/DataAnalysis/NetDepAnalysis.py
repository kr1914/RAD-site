import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import cv2 as cv
import numpy as np
import tools.tool as tool
import io
from scapy.all import rdpcap
from scapy.all import PcapReader


# 바이너리 형식으로 pcap 파일을 받아서 처리하는 경우
def process_pcap(binary_data):
    result = []
    with io.BytesIO(binary_data) as f:
        packets = PcapReader(f)

        packet_count = 0
        for i, packet in enumerate(packets):
            print(f"Packet {i+1}: {packet.summary()}")
            #print(packet.show(dump=True))  # 자세한 패킷 정보 출력 (문자열 형식)
            result.append(packet.show(dump=True))
            packet_count += 1
        # PcapReader는 반드시 close()로 종료해야 함
        packets.close()
    
    return result


st.header("pcap 분석")
# value = streamlit_image_coordinates("https://plantuml.com/imgw/img-e890b0fb49cf18a254ed383fa4710f81.png")
# st.write(value)
st.write("네트워크 구성 분석")

uploaded_file = st.file_uploader("Choose a .pcap file")

if uploaded_file is not None:
    try:
        # Read the uploaded file
        bytes_data = uploaded_file.getvalue()
    

        # 바이너리 데이터를 함수로 처리
        packets_info = process_pcap(bytes_data)
        
        st.write(packets_info)
        
    except Exception as e:
        st.error(f"bytes_data : {len(bytes_data)}")
        
        st.error(f"Error: {e}")
        




