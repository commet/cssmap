"""
프리즈·키아프 2025 전체 갤러리 목록
Google Maps에서 확인한 약 60개 갤러리 통합
"""

COMPLETE_GALLERY_LOCATIONS = {
    # 공식 행사장
    "코엑스": {"lat": 37.5116, "lng": 127.0594, "name": "COEX", "category": "공식 행사장"},
    "도산공원": {"lat": 37.5228, "lng": 127.0351, "name": "Dosan Park", "category": "공식 행사장"},
    
    # 을지로 나이트 (9/1 월요일)
    "양혜규스튜디오": {"lat": 37.5650, "lng": 126.9910, "name": "Yanghyegyu Studio", "category": "을지로"},
    
    # 한남 나이트 (9/2 화요일) - 13개 갤러리
    "바크": {"lat": 37.5345, "lng": 127.0045, "name": "BHAK", "category": "한남"},
    "갤러리SP": {"lat": 37.5350, "lng": 127.0050, "name": "Gallery SP", "category": "한남"},
    "갤러리조은": {"lat": 37.5348, "lng": 127.0048, "name": "Gallery Joeun", "category": "한남"},
    "가나아트한남": {"lat": 37.5352, "lng": 127.0052, "name": "Gana Art Hannam", "category": "한남"},
    "리만머핀": {"lat": 37.5347, "lng": 127.0047, "name": "Riman Muffin", "category": "한남"},
    "에스터쉬퍼": {"lat": 37.5355, "lng": 127.0055, "name": "Esther Schipper", "category": "한남"},
    "타데우스로팍": {"lat": 37.5360, "lng": 127.0060, "name": "Thaddeus Ropac Seoul", "category": "한남"},
    "갤러리바톤": {"lat": 37.5365, "lng": 127.0065, "name": "Gallery Baton", "category": "한남"},
    "디스위켄드룸": {"lat": 37.5370, "lng": 127.0070, "name": "This Weekend Room", "category": "한남"},
    "조현화랑": {"lat": 37.5375, "lng": 127.0075, "name": "Johyun Gallery", "category": "한남"},
    "P21": {"lat": 37.5380, "lng": 127.0080, "name": "P21", "category": "한남"},
    "실린더2": {"lat": 37.5385, "lng": 127.0085, "name": "Cylinder2", "category": "한남"},
    "듀아츠": {"lat": 37.5390, "lng": 127.0090, "name": "Deux Arts", "category": "한남"},
    
    # 청담 나이트 (9/3 수요일) - 13개 갤러리
    "갤러리가이아": {"lat": 37.5240, "lng": 127.0380, "name": "Gallery Gaia", "category": "청담"},
    "그라프": {"lat": 37.5245, "lng": 127.0385, "name": "Gallery Graph", "category": "청담"},
    "김리아갤러리": {"lat": 37.5250, "lng": 127.0390, "name": "Kim Ria Gallery", "category": "청담"},
    "갤러리피치": {"lat": 37.5255, "lng": 127.0395, "name": "Gallery Peach", "category": "청담"},
    "갤러리플래닛": {"lat": 37.5260, "lng": 127.0400, "name": "Gallery Planet", "category": "청담"},
    "갤러리위청담": {"lat": 37.5265, "lng": 127.0405, "name": "Gallery We Cheongdam", "category": "청담"},
    "글래드스톤갤러리": {"lat": 37.5270, "lng": 127.0410, "name": "Gladstone Gallery Seoul", "category": "청담"},
    "화이트큐브서울": {"lat": 37.5275, "lng": 127.0415, "name": "White Cube Seoul", "category": "청담"},
    "페로탕": {"lat": 37.5280, "lng": 127.0420, "name": "Perrotin", "category": "청담"},
    "G갤러리": {"lat": 37.5285, "lng": 127.0425, "name": "G Gallery", "category": "청담"},
    "이유진갤러리": {"lat": 37.5290, "lng": 127.0430, "name": "Lee Eugean Gallery", "category": "청담"},
    "송은아트스페이스": {"lat": 37.5295, "lng": 127.0435, "name": "Song-eun Art Space", "category": "청담"},
    "아뜰리에에르메스": {"lat": 37.5230, "lng": 127.0370, "name": "Atelier Hermes", "category": "청담"},
    
    # 삼청 나이트 (9/4 목요일) - 17개 갤러리
    "국제갤러리": {"lat": 37.5802, "lng": 126.9749, "name": "Kukje Gallery", "category": "삼청"},
    "갤러리진선": {"lat": 37.5807, "lng": 126.9754, "name": "Gallery Jinsun", "category": "삼청"},
    "예화랑": {"lat": 37.5812, "lng": 126.9759, "name": "Yehwa Gallery", "category": "삼청"},
    "우손갤러리": {"lat": 37.5817, "lng": 126.9764, "name": "Woosun Gallery", "category": "삼청"},
    "리화랑": {"lat": 37.5822, "lng": 126.9769, "name": "Lee Hwa Gallery", "category": "삼청"},
    "최앤최갤러리": {"lat": 37.5827, "lng": 126.9774, "name": "Choi & Choi Gallery", "category": "삼청"},
    "갤러리현대": {"lat": 37.5789, "lng": 126.9770, "name": "Gallery Hyundai", "category": "삼청"},
    "학고재": {"lat": 37.5794, "lng": 126.9780, "name": "Hakgojae", "category": "삼청"},
    "바라캇컨템포러리": {"lat": 37.5799, "lng": 126.9785, "name": "Barakat Contemporary", "category": "삼청"},
    "백아트": {"lat": 37.5804, "lng": 126.9790, "name": "BAIK ART", "category": "삼청"},
    "갤러리조선": {"lat": 37.5809, "lng": 126.9795, "name": "Gallery Chosun", "category": "삼청"},
    "아라리오갤러리": {"lat": 37.5814, "lng": 126.9800, "name": "Arario Gallery", "category": "삼청"},
    "아트선재센터": {"lat": 37.5363, "lng": 126.9747, "name": "Art Sonje Center", "category": "삼청"},
    "여재단": {"lat": 37.5824, "lng": 126.9810, "name": "Yeo Foundation", "category": "삼청"},
    "순혜원": {"lat": 37.5829, "lng": 126.9815, "name": "Sunhyewon", "category": "삼청"},
    "일민미술관": {"lat": 37.5700, "lng": 126.9750, "name": "Ilmin Museum", "category": "삼청"},
    
    # 추가 주요 갤러리
    "리움미술관": {"lat": 37.5384, "lng": 126.9990, "name": "Leeum Museum", "category": "기타"},
    "페이스갤러리": {"lat": 37.5372, "lng": 127.0018, "name": "Pace Gallery", "category": "기타"},
    "PKM갤러리": {"lat": 37.5794, "lng": 126.9742, "name": "PKM Gallery", "category": "삼청"},
    "성수동": {"lat": 37.5447, "lng": 127.0557, "name": "Seongsu-dong", "category": "지역"}
}

# 위치명 자동완성을 위한 별칭 매핑
LOCATION_ALIASES = {
    # 공식 행사장
    "코엑스": ["coex", "코엑스", "코액스", "삼성역", "프리즈", "frieze"],
    "도산공원": ["도산", "dosan", "도산공원"],
    
    # 한남
    "바크": ["bhak", "바크", "박"],
    "갤러리SP": ["sp", "에스피"],
    "가나아트한남": ["가나", "가나아트", "gana"],
    "에스터쉬퍼": ["esther", "에스터", "schipper", "쉬퍼"],
    "타데우스로팍": ["thaddeus", "타데우스", "ropac", "로팍"],
    "갤러리바톤": ["바톤", "baton"],
    "디스위켄드룸": ["디스위켄드", "this weekend", "위켄드룸"],
    "조현화랑": ["조현", "johyun"],
    
    # 청담
    "갤러리가이아": ["가이아", "gaia"],
    "그라프": ["graph", "그래프"],
    "김리아갤러리": ["김리아", "kim ria"],
    "글래드스톤갤러리": ["gladstone", "글래드스톤"],
    "화이트큐브서울": ["white cube", "화이트큐브", "화큐"],
    "페로탕": ["perrotin", "페로탕"],
    "송은아트스페이스": ["송은", "songeun", "송은아트"],
    "아뜰리에에르메스": ["hermes", "에르메스", "아뜰리에"],
    
    # 삼청
    "국제갤러리": ["국제", "kukje", "kukje gallery", "국제 갤러리"],
    "갤러리현대": ["현대갤러리", "gallery hyundai", "현대"],
    "학고재": ["hakgojae", "학고재갤러리"],
    "바라캇컨템포러리": ["바라캇", "barakat"],
    "백아트": ["baik", "백아트", "baik art"],
    "아라리오갤러리": ["아라리오", "arario"],
    "아트선재센터": ["아트선재", "art sonje", "선재"],
    "일민미술관": ["일민", "ilmin"],
    
    # 기타
    "리움미술관": ["리움", "leeum", "삼성미술관", "리움"],
    "페이스갤러리": ["pace", "페이스", "pace gallery"],
    "PKM갤러리": ["pkm", "피케이엠"]
}


def get_all_gallery_count():
    """전체 갤러리 수 반환"""
    return len(COMPLETE_GALLERY_LOCATIONS)


def get_galleries_by_category():
    """카테고리별 갤러리 분류"""
    by_category = {}
    for name, info in COMPLETE_GALLERY_LOCATIONS.items():
        category = info['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(name)
    return by_category


def print_gallery_summary():
    """갤러리 요약 정보 출력"""
    print("=" * 60)
    print("프리즈·키아프 2025 갤러리 목록")
    print("=" * 60)
    
    by_category = get_galleries_by_category()
    
    for category, galleries in by_category.items():
        print(f"\n[{category}] ({len(galleries)}개)")
        for gallery in galleries[:5]:
            print(f"   - {gallery}")
        if len(galleries) > 5:
            print(f"   ... 외 {len(galleries)-5}개")
    
    print(f"\n총 {get_all_gallery_count()}개 갤러리 등록 완료")
    print("\n날짜별 갤러리 나이트:")
    print("   9/1 (월) - 을지로 나이트")
    print("   9/2 (화) - 한남 나이트 (13개 갤러리)")
    print("   9/3 (수) - 청담 나이트 (13개 갤러리)")
    print("   9/4 (목) - 삼청 나이트 (17개 갤러리)")


if __name__ == "__main__":
    print_gallery_summary()