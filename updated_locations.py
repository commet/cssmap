"""
프리즈·키아프 2025 전체 갤러리 목록
Google Maps에서 확인한 실제 GPS 좌표
"""

COMPLETE_GALLERY_LOCATIONS = {
    # 공식 행사장
    "코엑스": {"lat": 37.5116828, "lng": 127.059151, "name": "COEX", "category": "공식 행사장"},
    "도산공원": {"lat": 37.5244813, "lng": 127.0353667, "name": "Dosan Park", "category": "공식 행사장"},
    
    # 을지로 나이트 (9/1 월요일)
    "양혜규스튜디오": {"lat": 37.5761171, "lng": 126.9995683, "name": "Yanghyegyu Studio", "category": "을지로"},
    
    # 한남 나이트 (9/2 화요일) - 13개 갤러리
    "바크": {"lat": 37.5428516, "lng": 127.0031988, "name": "BHAK", "category": "한남"},
    "갤러리SP": {"lat": 37.5382689, "lng": 126.9942755, "name": "Gallery SP", "category": "한남"},
    "갤러리조은": {"lat": 37.5380256, "lng": 127.0006167, "name": "Gallery Joeun", "category": "한남"},
    "가나아트한남": {"lat": 37.5266211, "lng": 126.9957442, "name": "Gana Art Hannam", "category": "한남"},
    "리만머핀": {"lat": 37.5349456, "lng": 126.997578, "name": "Lehmann Maupin", "category": "한남"},
    "에스더쉬퍼": {"lat": 37.54353, "lng": 127.0024031, "name": "Esther Schipper", "category": "한남"},
    "타데우스로팍": {"lat": 37.5368135, "lng": 127.0127126, "name": "Thaddeus Ropac Seoul", "category": "한남"},
    "갤러리바톤": {"lat": 37.5364166, "lng": 127.012126, "name": "Gallery Baton", "category": "한남"},
    "디스위켄드룸": {"lat": 37.54344, "lng": 127.0030903, "name": "This Weekend Room", "category": "한남"},
    "조현화랑": {"lat": 37.5558403, "lng": 127.0054318, "name": "Johyun Gallery", "category": "한남"},
    "P21": {"lat": 37.5401115, "lng": 126.9939098, "name": "P21", "category": "한남"},
    "실린더2": {"lat": 37.5311286, "lng": 126.9716807, "name": "Cylinder2", "category": "한남"},
    "두아르트": {"lat": 37.535449, "lng": 127.0102429, "name": "Deux Arts", "category": "한남"},
    
    # 청담 나이트 (9/3 수요일) - 13개 갤러리
    "갤러리가이아": {"lat": 37.5249303, "lng": 127.0482668, "name": "Gallery Gaia", "category": "청담"},
    "갤러리그라프": {"lat": 37.5299928, "lng": 127.0536057, "name": "Gallery Graph", "category": "청담"},
    "김리아갤러리": {"lat": 37.52638559999999, "lng": 127.0422348, "name": "Kim Rhea Gallery", "category": "청담"},
    "갤러리피치": {"lat": 37.52502, "lng": 127.04836, "name": "Gallery Peach", "category": "청담"},
    "갤러리플래닛": {"lat": 37.5288088, "lng": 127.0395477, "name": "Gallery Planet", "category": "청담"},
    "갤러리위청담": {"lat": 37.5251373, "lng": 127.0440522, "name": "Gallery We Cheongdam", "category": "청담"},
    "글래드스톤갤러리": {"lat": 37.5235149, "lng": 127.0476853, "name": "Gladstone Gallery Seoul", "category": "청담"},
    "화이트큐브서울": {"lat": 37.52511419999999, "lng": 127.0412635, "name": "White Cube Seoul", "category": "청담"},
    "페로탕": {"lat": 37.52385099999999, "lng": 127.0385823, "name": "Perrotin", "category": "청담"},
    "G갤러리": {"lat": 37.5277917, "lng": 127.0451072, "name": "G Gallery", "category": "청담"},
    "이유진갤러리": {"lat": 37.5279669, "lng": 127.0485834, "name": "Lee Eugean Gallery", "category": "청담"},
    "송은아트스페이스": {"lat": 37.526215, "lng": 127.0471125, "name": "Song-eun Art Space", "category": "청담"},
    "아뜰리에에르메스": {"lat": 37.5236899, "lng": 127.0360833, "name": "Atelier Hermes", "category": "청담"},
    
    # 삼청 나이트 (9/4 목요일) - 17개 갤러리
    "국제갤러리": {"lat": 37.5802, "lng": 126.9749, "name": "Kukje Gallery", "category": "삼청"},
    "갤러리진선": {"lat": 37.5775848, "lng": 126.9804062, "name": "Gallery Jinsun", "category": "삼청"},
    "예화랑": {"lat": 37.5797718, "lng": 126.9824513, "name": "Yehwa Gallery", "category": "삼청"},
    "우손갤러리": {"lat": 37.577931, "lng": 126.9809031, "name": "Woosun Gallery", "category": "삼청"},
    "이화익갤러리": {"lat": 37.5794033, "lng": 126.9820844, "name": "Lee Hwa Ik Gallery", "category": "삼청"},
    "초이앤초이갤러리": {"lat": 37.5783798, "lng": 126.9817695, "name": "Choi & Choi Gallery", "category": "삼청"},
    "갤러리현대": {"lat": 37.5789, "lng": 126.9770, "name": "Gallery Hyundai", "category": "삼청"},
    "학고재": {"lat": 37.5794068, "lng": 126.9799879, "name": "Hakgojae", "category": "삼청"},
    "바라캇컨템포러리": {"lat": 37.5788088, "lng": 126.9811406, "name": "Barakat Contemporary", "category": "삼청"},
    "백아트": {"lat": 37.5788, "lng": 126.98126, "name": "BAIK ART", "category": "삼청"},
    "갤러리조선": {"lat": 37.5770208, "lng": 126.982322, "name": "Gallery Chosun", "category": "삼청"},
    "아라리오갤러리": {"lat": 37.5797018, "lng": 126.9825973, "name": "Arario Gallery", "category": "삼청"},
    "아트선재센터": {"lat": 37.5363, "lng": 126.9747, "name": "Art Sonje Center", "category": "삼청"},
    "여재단": {"lat": 37.5772373, "lng": 126.9807562, "name": "Yeo Foundation", "category": "삼청"},
    "전혁림": {"lat": 37.5772055, "lng": 126.9810493, "name": "Jeon Hyeok Lim", "category": "삼청"},
    "우양미술관": {"lat": 37.5813379, "lng": 126.9790324, "name": "Wooyang Museum", "category": "삼청"},
    "PKM갤러리": {"lat": 37.5794, "lng": 126.9742, "name": "PKM Gallery", "category": "삼청"},
    
    # 추가 주요 갤러리
    "리움미술관": {"lat": 37.5384, "lng": 126.9990, "name": "Leeum Museum", "category": "기타"},
    "페이스갤러리": {"lat": 37.5372, "lng": 127.0018, "name": "Pace Gallery", "category": "기타"},
    "가나아트센터": {"lat": 37.5731, "lng": 126.9719, "name": "Gana Art Center", "category": "기타"},
    "대림미술관": {"lat": 37.556885, "lng": 126.9176883, "name": "Daelim Museum", "category": "기타"},
    "성수동": {"lat": 37.5447, "lng": 127.0557, "name": "Seongsu-dong", "category": "지역"},
    
    # 추가 갤러리들
    "K현대미술관": {"lat": 37.5722388, "lng": 127.005175, "name": "K Museum of Contemporary Art", "category": "기타"},
    "갤러리사이먼": {"lat": 37.5259302, "lng": 127.0459896, "name": "Gallery Simon", "category": "청담"},
    "아트사이드갤러리": {"lat": 37.5776844, "lng": 126.9807936, "name": "Artside Gallery", "category": "삼청"},
    "인사아트센터": {"lat": 37.5738238, "lng": 126.9879593, "name": "Insa Art Center", "category": "기타"},
    "갤러리라벨": {"lat": 37.5213419, "lng": 127.0406271, "name": "Gallery Ravel", "category": "청담"},
    "갤러리인": {"lat": 37.5765907, "lng": 126.9819523, "name": "Gallery IN", "category": "삼청"},
    "갤러리도스": {"lat": 37.526265, "lng": 127.0484457, "name": "Gallery DOS", "category": "청담"},
    "갤러리마크": {"lat": 37.5305638, "lng": 127.0390565, "name": "Gallery Mark", "category": "청담"},
    "아트파크": {"lat": 37.5770825, "lng": 126.9820896, "name": "Art Park", "category": "삼청"},
    "갤러리이배": {"lat": 37.5794663, "lng": 126.9823621, "name": "Gallery Yeh", "category": "삼청"},
    "갤러리미르": {"lat": 37.5779436, "lng": 126.9808601, "name": "Gallery Mir", "category": "삼청"},
    "갤러리도올": {"lat": 37.5774948, "lng": 126.9803969, "name": "Gallery Doll", "category": "삼청"},
    "갤러리빔": {"lat": 37.5770071, "lng": 126.9823322, "name": "Gallery Bim", "category": "삼청"},
    "갤러리세줄": {"lat": 37.578038, "lng": 126.9810562, "name": "Gallery Sejul", "category": "삼청"},
    "갤러리소소": {"lat": 37.5766488, "lng": 126.9818959, "name": "Gallery SoSo", "category": "삼청"},
    "갤러리율": {"lat": 37.5791263, "lng": 126.9819015, "name": "Gallery Yul", "category": "삼청"},
    "갤러리토": {"lat": 37.5767563, "lng": 126.9818988, "name": "Gallery Teo", "category": "삼청"},
    "갤러리이안": {"lat": 37.5773869, "lng": 126.9811119, "name": "Gallery IAN", "category": "삼청"},
    "갤러리룩스": {"lat": 37.5775577, "lng": 126.9806291, "name": "Gallery Lux", "category": "삼청"},
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
    "에스더쉬퍼": ["esther", "에스터", "schipper", "쉬퍼"],
    "타데우스로팍": ["thaddeus", "타데우스", "ropac", "로팍"],
    "갤러리바톤": ["바톤", "baton"],
    "디스위켄드룸": ["디스위켄드", "this weekend", "위켄드룸"],
    "조현화랑": ["조현", "johyun"],
    
    # 청담
    "갤러리가이아": ["가이아", "gaia"],
    "갤러리그라프": ["graph", "그래프"],
    "김리아갤러리": ["김리아", "kim rhea"],
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