"""
KMZ/KML 파일 파서
Google Maps에서 다운로드한 갤러리 위치 정보 추출
"""

import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
import json
import re

class KMZParser:
    """KMZ 파일에서 갤러리 정보 추출"""
    
    def __init__(self, kmz_path: str = None):
        self.kmz_path = kmz_path
        self.galleries = {}
        
    def parse_kmz(self, kmz_path: str) -> Dict[str, List[Dict]]:
        """
        KMZ 파일 파싱 (KMZ = 압축된 KML)
        
        Returns:
            카테고리별 갤러리 정보
        """
        galleries_by_category = {}
        
        try:
            # KMZ는 ZIP 파일
            with zipfile.ZipFile(kmz_path, 'r') as kmz:
                # KML 파일 찾기
                for filename in kmz.namelist():
                    if filename.endswith('.kml'):
                        with kmz.open(filename) as kml_file:
                            kml_content = kml_file.read()
                            galleries_by_category = self.parse_kml(kml_content)
                            break
        except Exception as e:
            print(f"KMZ 파싱 오류: {e}")
            
        return galleries_by_category
    
    def parse_kml(self, kml_content: bytes) -> Dict[str, List[Dict]]:
        """
        KML 내용 파싱
        
        Returns:
            갤러리 정보 딕셔너리
        """
        galleries = {}
        
        try:
            # XML 파싱
            root = ET.fromstring(kml_content)
            
            # KML 네임스페이스
            ns = {'kml': 'http://www.opengis.net/kml/2.2'}
            
            # 모든 Placemark (위치 마커) 찾기
            for folder in root.findall('.//kml:Folder', ns):
                folder_name = folder.find('kml:name', ns)
                if folder_name is not None:
                    category = folder_name.text
                    galleries[category] = []
                    
                    for placemark in folder.findall('.//kml:Placemark', ns):
                        gallery = self.extract_placemark_info(placemark, ns)
                        if gallery:
                            galleries[category].append(gallery)
        
        except Exception as e:
            print(f"KML 파싱 오류: {e}")
            
        return galleries
    
    def extract_placemark_info(self, placemark, ns) -> Dict:
        """
        Placemark에서 갤러리 정보 추출
        """
        gallery = {}
        
        # 이름
        name = placemark.find('kml:name', ns)
        if name is not None:
            gallery['name'] = name.text
        
        # 설명
        description = placemark.find('kml:description', ns)
        if description is not None:
            gallery['description'] = description.text
        
        # 좌표
        coordinates = placemark.find('.//kml:coordinates', ns)
        if coordinates is not None:
            coords = coordinates.text.strip()
            if coords:
                # 좌표 형식: longitude,latitude,altitude
                parts = coords.split(',')
                if len(parts) >= 2:
                    gallery['longitude'] = float(parts[0])
                    gallery['latitude'] = float(parts[1])
        
        return gallery if 'name' in gallery else None
    
    def extract_coordinates(self, coord_string: str) -> Tuple[float, float]:
        """
        좌표 문자열에서 위도/경도 추출
        """
        try:
            parts = coord_string.strip().split(',')
            if len(parts) >= 2:
                lng = float(parts[0])
                lat = float(parts[1])
                return lat, lng
        except:
            pass
        return None, None


# 지도에서 확인한 갤러리 목록을 직접 정의
GALLERY_LOCATIONS = {
    "공식 행사장": {
        "코엑스": {"lat": 37.5116, "lng": 127.0594, "name_en": "COEX"},
        "도산공원": {"lat": 37.5228, "lng": 127.0351, "name_en": "Dosan Park"}
    },
    
    "을지로 나이트 (9/1 월)": {
        "양혜규 스튜디오": {"lat": 37.5650, "lng": 126.9910, "name_en": "Yanghyegyu Studio"}
    },
    
    "한남 나이트 (9/2 화)": {
        "바크": {"lat": 37.5345, "lng": 127.0045, "name_en": "BHAK"},
        "갤러리SP": {"lat": 37.5350, "lng": 127.0050, "name_en": "Gallery SP"},
        "갤러리조은": {"lat": 37.5348, "lng": 127.0048, "name_en": "Gallery Joeun"},
        "가나아트 한남": {"lat": 37.5352, "lng": 127.0052, "name_en": "Gana Art Hannam"},
        "리만머핀": {"lat": 37.5347, "lng": 127.0047, "name_en": "Riman Muffin"},
        "에스터 쉬퍼": {"lat": 37.5355, "lng": 127.0055, "name_en": "Esther Schipper"},
        "타데우스 로팍 서울": {"lat": 37.5360, "lng": 127.0060, "name_en": "Thaddeus Ropac Seoul"},
        "갤러리바톤": {"lat": 37.5365, "lng": 127.0065, "name_en": "Gallery Baton"},
        "디스위켄드룸": {"lat": 37.5370, "lng": 127.0070, "name_en": "This Weekend Room"},
        "조현화랑": {"lat": 37.5375, "lng": 127.0075, "name_en": "Johyun Gallery"},
        "P21": {"lat": 37.5380, "lng": 127.0080, "name_en": "P21"},
        "실린더2": {"lat": 37.5385, "lng": 127.0085, "name_en": "Cylinder2"},
        "듀아츠": {"lat": 37.5390, "lng": 127.0090, "name_en": "Deux Arts"}
    },
    
    "청담 나이트 (9/3 수)": {
        "갤러리가이아": {"lat": 37.5240, "lng": 127.0380, "name_en": "Gallery Gaia"},
        "그라프": {"lat": 37.5245, "lng": 127.0385, "name_en": "Gallery Graph"},
        "김리아갤러리": {"lat": 37.5250, "lng": 127.0390, "name_en": "Kim Ria Gallery"},
        "갤러리피치": {"lat": 37.5255, "lng": 127.0395, "name_en": "Gallery Peach"},
        "갤러리플래닛": {"lat": 37.5260, "lng": 127.0400, "name_en": "Gallery Planet"},
        "갤러리위 청담": {"lat": 37.5265, "lng": 127.0405, "name_en": "Gallery We Cheongdam"},
        "글래드스톤 갤러리": {"lat": 37.5270, "lng": 127.0410, "name_en": "Gladstone Gallery Seoul"},
        "화이트큐브 서울": {"lat": 37.5275, "lng": 127.0415, "name_en": "White Cube Seoul"},
        "페로탕": {"lat": 37.5280, "lng": 127.0420, "name_en": "Perrotin"},
        "G갤러리": {"lat": 37.5285, "lng": 127.0425, "name_en": "G Gallery"},
        "이유진갤러리": {"lat": 37.5290, "lng": 127.0430, "name_en": "Lee Eugean Gallery"},
        "송은아트스페이스": {"lat": 37.5295, "lng": 127.0435, "name_en": "Song-eun Art Space"},
        "아뜰리에 에르메스": {"lat": 37.5230, "lng": 127.0370, "name_en": "Atelier Hermes"}
    },
    
    "삼청 나이트 (9/4 목)": {
        "국제갤러리": {"lat": 37.5802, "lng": 126.9749, "name_en": "Kukje Gallery"},
        "갤러리진선": {"lat": 37.5807, "lng": 126.9754, "name_en": "Gallery Jinsun"},
        "예화랑": {"lat": 37.5812, "lng": 126.9759, "name_en": "Yehwa Gallery"},
        "우손갤러리": {"lat": 37.5817, "lng": 126.9764, "name_en": "Woosun Gallery"},
        "리화랑": {"lat": 37.5822, "lng": 126.9769, "name_en": "Lee Hwa Gallery"},
        "최앤최갤러리": {"lat": 37.5827, "lng": 126.9774, "name_en": "Choi & Choi Gallery"},
        "갤러리현대": {"lat": 37.5789, "lng": 126.9770, "name_en": "Gallery Hyundai"},
        "학고재": {"lat": 37.5794, "lng": 126.9780, "name_en": "Hakgojae"},
        "바라캇컨템포러리": {"lat": 37.5799, "lng": 126.9785, "name_en": "Barakat Contemporary"},
        "백아트": {"lat": 37.5804, "lng": 126.9790, "name_en": "BAIK ART"},
        "갤러리조선": {"lat": 37.5809, "lng": 126.9795, "name_en": "Gallery Chosun"},
        "아라리오갤러리": {"lat": 37.5814, "lng": 126.9800, "name_en": "Arario Gallery"},
        "아트선재센터": {"lat": 37.5363, "lng": 126.9747, "name_en": "Art Sonje Center"},
        "여재단": {"lat": 37.5824, "lng": 126.9810, "name_en": "Yeo Foundation"},
        "순혜원": {"lat": 37.5829, "lng": 126.9815, "name_en": "Sunhyewon"},
        "일민미술관": {"lat": 37.5700, "lng": 126.9750, "name_en": "Ilmin Museum"}
    }
}


def generate_updated_locations():
    """
    프로젝트에서 사용할 수 있는 형태로 갤러리 목록 생성
    """
    all_galleries = {}
    
    for category, galleries in GALLERY_LOCATIONS.items():
        for name_ko, info in galleries.items():
            # 키는 한글명으로
            all_galleries[name_ko] = {
                "lat": info["lat"],
                "lng": info["lng"],
                "name": name_ko,
                "name_en": info["name_en"],
                "category": category
            }
    
    return all_galleries


def main():
    """사용 예제"""
    
    print("=" * 60)
    print("프리즈·키아프 2025 갤러리 목록")
    print("=" * 60)
    
    galleries = generate_updated_locations()
    
    # 카테고리별 정리
    by_category = {}
    for name, info in galleries.items():
        category = info['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(name)
    
    # 출력
    for category, gallery_list in by_category.items():
        print(f"\n📍 {category}")
        print(f"   갤러리 수: {len(gallery_list)}개")
        for gallery in gallery_list[:5]:  # 처음 5개만 표시
            print(f"   - {gallery}")
        if len(gallery_list) > 5:
            print(f"   ... 외 {len(gallery_list)-5}개")
    
    print(f"\n총 {len(galleries)}개 갤러리 등록")
    
    # JSON 파일로 저장
    with open('gallery_locations.json', 'w', encoding='utf-8') as f:
        json.dump(galleries, f, ensure_ascii=False, indent=2)
    print("\n✅ gallery_locations.json 파일 생성 완료")
    
    # KMZ 파일이 있다면 파싱
    print("\n💡 KMZ 파일 파싱 방법:")
    print("1. Google Maps에서 KMZ 다운로드")
    print("2. parser = KMZParser()")
    print("3. galleries = parser.parse_kmz('your_map.kmz')")
    print("4. 추출된 좌표를 프로젝트에 통합")


if __name__ == "__main__":
    main()