"""
4단계: characters.json을 pilot.js로 변환
"""
import json


def json_to_js(json_file='characters.json', js_file='pilot.js'):
    """JSON 파일을 JavaScript 형식으로 변환"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write('const sampleData = ')
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write(';\n')
        
        print(f"✓ {js_file} 생성 완료 ({len(data)}개 캐릭터)")
        return True
    except Exception as e:
        print(f"✗ {js_file} 생성 실패: {e}")
        return False


if __name__ == "__main__":
    json_to_js()
