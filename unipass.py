# 2021.07.10
# 국가관세종합정보망 OPEN API를 활용한 수입화물 진행정보 조회 Python GUI 프로그램
# TO DO LIST = [GUI 재정의, 정보 조금 더 많이 표시, 반복조회, 다건조회, 에러코드]

# API 호출을 위한 requests
# xml parsing을 위한 ElementTree
# 날짜, 시간 사용을 위한 datetime
# GUI 구현을 위한 tkinter
import requests
import xml.etree.ElementTree as ET
import datetime
import tkinter
import tkinter.ttk as ttk
from tkinter.constants import END

main_window = tkinter.Tk() # GUI 프로그래밍 시작
main_window.title('통관 조회 프로그램') # 프로그램 상단 이름 설정
main_window.geometry('640x480') # 창 크기 설정
main_window.resizable(False, False) # 창 크기 조절 불가

#프로그램 메인 메시지 출력 
label_main = tkinter.Label(main_window, text='통관 조회를 위한 프로그램입니다.')
label_main.pack()

#결과값을 출력할 Text창 생성
output_search = tkinter.Text(main_window, width=70, height=20)
output_search.pack()
output_search.insert(1.0, "이곳에 결과값이 출력됩니다.")

#운송장번호를 입력할 Entry창 생성
input_hbl = tkinter.Entry(main_window, width=50)
input_hbl.pack()
input_hbl.insert(tkinter.END, "조회 할 운송장번호를 입력하세요")

#년도 선택을 위한 메시지 출력
label_year = tkinter.Label(main_window, text='년도를 선택해주세요. \n기본 값은 올해 년도입니다.')
label_year.pack()

this_year=datetime.datetime.today().year # 현재 년도를 불러옴
years = [str(i)+'년' for i in range(2013, this_year+2)] # 2013년~(현재 년도+1)까지 리스트에 저장
years.sort(reverse=True) # 저장한 년도를 내림차순으로 정렬
combobox_year = ttk.Combobox(main_window, width=10, height=0, values=years, state="readonly") #읽기 전용 콤보박스 생성
combobox_year.current(1) # 콤보박스 기본 설정값은 현재 년도(1번째 인덱스)
combobox_year.pack()

def get_info(): # API 호출 함수
    
    # 조회할 운송장 번호 입력
    global crkyCn, hblNo, blYy, host, path, payload, url, response, root # API 호출에 사용되는 변수를 전역변수로 설정
    global num # API 호출에 사용되는 변수를 전역변수로 설정
    global csclprgsStts, prgsStts, prnm, shedNm, prcsDttm, rlbrCn # API에 출력에 사용되는 변수를 전역변수로 설정
    # 통관진행상태, 진행상태, 품명, 장치장명, 처리일시, 반출입내용

    crkyCn = 'empty' # 개인 Key 값
    hblNo = input_hbl.get() # 운송장번호
    blYy = combobox_year.get() # API 호출 시 사용되는 

    # REST API 호출을 위해 URL을 만듦
    host = 'https://unipass.customs.go.kr:38010'
    path = '/ext/rest/cargCsclPrgsInfoQry/retrieveCargCsclPrgsInfo'
    payload = {'crkyCn':crkyCn, 'hblNo':hblNo, 'blYy': blYy}
    url = host + path

    # API를 호출 후 xml을 response에 저장
    response = requests.get(url,params=payload)
    # 문자열로 된 XML 가져오기
    root = ET.fromstring(response.text)
    
    #문자열 인덱싱 후 년도 출력
    raw_prcsDttm = root.findall('.//prcsDttm')[0].text
    raw_year = raw_prcsDttm[:4]
    raw_month = raw_prcsDttm[4:6]
    raw_day = raw_prcsDttm[6:8]
    raw_time = raw_prcsDttm[8:10]
    raw_minute = raw_prcsDttm[10:12]
    raw_second = raw_prcsDttm[12:14]
    kor_date = raw_year + '-' + raw_month + '-' + raw_day + ' ' + raw_time + ':' + raw_second + ':' + raw_second
    
    prcsDttm = "처리일시 : " + kor_date
    csclprgsStts = "진행상태 : " + (root.findall('.//csclPrgsStts')[0].text)
    prnm = "  품명   : " + (root.findall('.//prnm')[0].text)
    shedNm = "장치장명 : " + (root.findall('.//shedNm')[0].text)

def print_info(): # API 출력 후 받아온 값을 출력하는 함수
    try: # API 호출 시도
        get_info()
    except: # API 호출 시도 후 에러 발생 시 에러 메시지 출력
        error_message = '올바른 운송장번호를 입력해주세요!'
        for t in error_message:
            output_search.insert(END, t)
        output_search.insert(END, "\n")
    else:
        for t in prcsDttm: # 처리일시 출력
            output_search.insert(END, t)
        output_search.insert(END, "\n")
        for t in csclprgsStts: # 통관진행상태 출력
            output_search.insert(END, t)
        output_search.insert(END, "\n")
        for t in prnm: # 품명 출력
            output_search.insert(END, t)
        output_search.insert(END, "\n")
        for t in shedNm: # 장치장명 출력
            output_search.insert(END, t)
        output_search.insert(END, "\n")
        output_search.insert(END, "\n")
        for t in range(0, 70): # 구분선 출력
            output_search.insert(END, '-')
        output_search.insert(END, "\n")
        output_search.insert(END, "\n")

def search(): # 조회 버튼 클릭 시 실행되는 함수
    output_search.delete('1.0', END) # output_search의 모든 내용 삭제
    listbox_recent_list.insert(0, input_hbl.get()) # 조회한 운송장번호를 최근 운송장번호 리스트에 추가
    print_info() # API 출력 후 받아온 값을 출력하는 함수

# 조회 버튼 생성
btn_search = tkinter.Button(main_window, width=5, height=2, text='조회', command=search)
btn_search.pack()

#최근 운송장번호 리스트 관련 메시지 출력 
label_recent_list = tkinter.Label(main_window, text='최근 조회하신 운송장번호 목록입니다.')
label_recent_list.pack()

#최근 운송장번호 리스트 생성
listbox_recent_list = tkinter.Listbox(main_window, selectmode='extended', height=0)
listbox_recent_list.pack()

def delete_all(): # 최근 운송장번호 리스트의 내용을 모두 삭제하는 함수
    listbox_recent_list.delete(0, END)

# 최근 운송장번호 리스트 전체 삭제 버튼 생성
btn_delete_all = tkinter.Button(main_window, width=15, height=1, text='목록 전체 삭제', command=delete_all)
btn_delete_all.pack()

main_window.mainloop() # GUI 프로그래밍 종료