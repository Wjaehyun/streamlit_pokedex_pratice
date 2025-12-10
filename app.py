import streamlit as st

# 새로 불러와졌는지 terminal에서 체크
print("page reloaded")
st.set_page_config(
    page_title="포켓몬 도감",
    page_icon="./images/monsterball.png"
)
# custom css 반영을 위한 markdown
st.markdown("""
<style>
img {
    max_height: 300px;
}
</style>
""", unsafe_allow_html=True)

st.title("streamlit 포켓몬 도감")
st.markdown("**포켓몬**을 하나씩 추가해서 도감을 채워보세요!")

type_emoji_dict = {
    "노말": "⚪️",
    "불꽃": "🔥",
    "물": "💧",
    "전기": "⚡",
    "풀": "🌿",
    "얼음": "❄️",
    "격투": "🥊",
    "독": "☠️",
    "땅": "🟫",
    "비행": "🪽",
    "에스퍼": "🥄",
    "벌레": "🐛",
    "바위": "🪨",
    "고스트": "👻",
    "드래곤": "🐉",
    "악": "😈",
    "강철": "⚙️",
    "페어리": "🧚"
}

initial_pokemons = [
     {
    "name": "피카츄",
    "types": ["전기"],
    "image_url": 'images/피카츄.webp'
    },
    {
    "name": "누오",
    "types": ["물", "땅"],
    "image_url": "images/누오.webp"
    },
    {
    "name": "갸라도스",
    "types": ["물", "비행"],
    "image_url": "images/갸라도스.webp"
    },
        {
    "name": "개굴닌자",
    "types": ["물"],
    "image_url": "images/개굴닌자.webp"
    },
    {
    "name": "루카리오",
    "types": ["격투", "강철"],
    "image_url": "images/루카리오.webp"
    },  
    {
    "name": "에이스번",
    "types": ["불꽃"],
    "image_url": "images/에이스번.webp"
    }
]

example_pokemon = {
     "name": "알로라 디그다",
     "types": ["땅", "강철"],
     "image_url": "images/알로라_디그다.png"
 }

# streamlit은 추가 업로드마다 새롭게 파일을 읽기 때문에
# 세션을 남겨야 추가된 포켓몬이 덮어쓰기 되지 않는다.
# 페이지를 지우거나 새로고침 할 때까지 남아있다.
if 'pokemons' not in st.session_state:
    st.session_state.pokemons = initial_pokemons


# toggle을 이용한 form 자동완성
auto_complete = st.toggle("예시 데이터로 채우기")
print("page_reload, auto_complete", auto_complete)
# 포켓몬 추가 버튼
with st.form(key="form"):
    col1, col2 = st.columns(2)
    # 이름 입력
    with col1:
        name = st.text_input(
            label="포켓몬 이름",
            # toggle 폼 자동 완성
            value=example_pokemon["name"] if auto_complete else ""
        )
    # 타입 선택
    with col2:
        types = st.multiselect(
            label="포켓몬 타입",
            options=list(type_emoji_dict.keys()),
            # 타입은 2개까지만
            max_selections=2,
            # toggle 폼 자동 완성
            default=example_pokemon["types"] if auto_complete else []
        )
    # 이미지 추가하기
    image_url = st.text_input(
        label="포켓몬 이미지 URL",
        # toggle 폼 자동 완성
        value=example_pokemon["image_url"] if auto_complete else ""
    )
    # 업로드
    submit = st.form_submit_button(label="Submit")
    if submit:
        # 전부 입력해야 업로드 되도록 예외 처리
        if not name:
            st.error("포켓몬의 이름을 입력해주세요.")
        elif len(types) == 0:
            st.error("포켓먼의 타입을 적어도 한 개 선택해주세요.")
        else:
            st.success("포켓몬을 추가할 수 있습니다.")
            st.session_state.pokemons.append({
                "name": name,
                "types": types,
                # 이미지가 있을 때는 이미지, 없으면 기본이미지
                "image_url": image_url if image_url else "./images/default.png"
            })


# 포켓몬을 이름/이미지/타입 출력
for i in range(0, len(st.session_state.pokemons), 3):
    # 3개씩 번호대로 출력
    row_pokemons = st.session_state.pokemons[i:i+3]
    cols = st.columns(3)
    for j in range(len(row_pokemons)):
        with cols[j]:
            pokemon = row_pokemons[j]
            with st.expander(label=f"**{i+1+j}. {pokemon['name']}**", expanded = True):
                st.image(pokemon["image_url"])
                emoji_types = [f"{type_emoji_dict[x]} {x}" for x in pokemon["types"]]
                st.text(" / ".join(emoji_types))
                # 삭제 버튼을 박스 크기에 맞게 제작/조절
                delete_button = st.button(label="삭제", key=i+j, use_container_width=True)
                if delete_button:
                    print("delete button clicked!")
                    del st.session_state.pokemons[i+j]
                    # rerun()으로 reload동작을 바로 반영/원하는 포켓몬 삭제 가능
                    st.rerun()
