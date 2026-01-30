"""
1단계: Selenium을 사용하여 HTML 다운로드
캐릭터 페이지에서 <table class="unit_list_table"> 추출
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# --- 설정 ---
NOSP_URL = "https://appmedia.jp/ggene_eternal/78594845"
SP_URL = "https://appmedia.jp/ggene_eternal/79406921"


def setup_driver():
    """Chrome 드라이버 설정"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    try:
        # webdriver-manager 사용 (자동으로 ChromeDriver 다운로드)
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except ImportError:
        # webdriver-manager 없으면 기본 방식
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"✗ ChromeDriver 초기화 실패: {e}")
            print("\n해결 방법:")
            print("  1. pip install webdriver-manager")
            print("  2. 또는 ChromeDriver 수동 설치: https://chromedriver.chromium.org/")
            print("  3. 또는 수동으로 HTML 다운로드")
            return None
    except Exception as e:
        print(f"✗ ChromeDriver 초기화 실패: {e}")
        return None


def download_character_table(url, output_file, description):
    """URL에서 캐릭터 테이블 다운로드"""
    print(f"\n{'='*60}")
    print(f"{description} 다운로드 중...")
    print(f"URL: {url}")
    print('='*60)
    
    driver = setup_driver()
    if not driver:
        return False
    
    try:
        driver.get(url)
        print("⏳ 페이지 로딩 대기 중...")
        time.sleep(5)  # 페이지 로딩 대기
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # <table class="unit_list_table"> 찾기
        table = soup.find('table', class_='unit_list_table')
        
        if table:
            rows = table.find_all('tbody', class_='chara_tbody')
            print(f"✅ unit_list_table 발견! ({len(rows)}개 캐릭터)")
            
            # HTML 파일로 저장
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(table))
            
            print(f"✓ {output_file} 저장 완료")
            
            # 미리보기
            print(f"\n📄 테이블 구조 미리보기:")
            print(f"  - 총 캐릭터 수: {len(rows)}")
            if rows:
                first_char = rows[0]
                name_tag = first_char.find('a')
                if name_tag:
                    name = name_tag.get_text(strip=True)
                    print(f"  - 첫 번째 캐릭터: {name}")
            
            return True
            
        else:
            print("✗ unit_list_table을 찾을 수 없습니다!")
            
            # 디버그: 전체 페이지 저장
            debug_file = output_file.replace('.html', '_debug.html')
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"🔍 디버그용 전체 페이지 저장: {debug_file}")
            
            return False
            
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        driver.quit()


def main():
    """메인 실행"""
    print("="*60)
    print("캐릭터 HTML 다운로드 시작")
    print("="*60)
    
    # NO SP 다운로드
    nosp_success = download_character_table(
        NOSP_URL, 
        "nonsp.html", 
        "NO SP 캐릭터"
    )
    
    # SP 다운로드
    sp_success = download_character_table(
        SP_URL, 
        "sp.html", 
        "SP 캐릭터"
    )
    
    # 결과 출력
    print("\n" + "="*60)
    if nosp_success and sp_success:
        print("✓ 모든 다운로드 완료!")
        print("="*60)
        print("\n생성된 파일:")
        print("  - nonsp.html")
        print("  - sp.html")
    else:
        print("✗ 일부 다운로드 실패")
        print("="*60)
        if not nosp_success:
            print("  ✗ nonsp.html 실패")
        if not sp_success:
            print("  ✗ sp.html 실패")
        
        print("\n수동 다운로드 방법:")
        print(f"  1. 브라우저에서 {NOSP_URL} 접속")
        print("  2. 개발자 도구 (F12) 열기")
        print("  3. Elements 탭에서 <table class=\"unit_list_table\"> 찾기")
        print("  4. 우클릭 → Copy → Copy element")
        print("  5. 텍스트 에디터에 붙여넣고 nonsp.html로 저장")
        print("  6. SP도 동일하게 진행")
    
    print()


if __name__ == "__main__":
    main()
