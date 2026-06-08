import streamlit as st
import json
import csv
import io
from datetime import datetime
from pathlib import Path

# ─── 경로 설정 ───
DATA_DIR = Path("data")
TERMS_FILE = DATA_DIR / "terms.json"
PROMPTS_FILE = DATA_DIR / "prompts.json"
SAMPLES_FILE = DATA_DIR / "samples.json"


# ─── 데이터 로드/저장 ───
def load_json(filepath):
    """JSON 파일 로드. 없으면 빈 리스트 반환."""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return []


def save_json(filepath, data):
    """JSON 파일 저장."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_terms():
    return load_json(TERMS_FILE)


def load_prompts():
    return load_json(PROMPTS_FILE)


def load_samples():
    return load_json(SAMPLES_FILE)


def save_terms(data):
    save_json(TERMS_FILE, data)


def save_samples(data):
    save_json(SAMPLES_FILE, data)


# ─── 페이지 설정 ───
st.set_page_config(
    page_title="UX 라이팅 도구",
    page_icon="✍️",
    layout="wide"
)
st.title("✍️ UX 라이팅 도구")
st.caption("용어집 검색 · Best/Worst 사례 · 데이터 관리")

# ─── 데이터 로드 ───
terms_db = load_terms()
prompts_db = load_prompts()
samples_db = load_samples()

# ─── 탭 구성 ───
tab1, tab2, tab3, tab4 = st.tabs([
    "✍  소개",
    "📖 용어집",
    "✅ Best/Worst 사례",
    "⚙️ 관리"
])

# ════════════════════════════════════════
# 탭 1: 한컴 UX 라이팅 소개
# ════════════════════════════════════════
with tab1:
    st.header("✍️ 한컴 UX 라이팅이란?")
    st.caption("사용자가 서비스를 쉽고 편안하게 이용할 수 있도록 인터페이스 문구를 설계하는 일입니다.")

    st.markdown("---")

    # ─── 핵심 원칙 ───
    st.subheader("📌 핵심 원칙")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🧑 사람 중심")
        st.markdown("""
        - 사용자를 탓하지 않는 톤
        - 기술 용어 대신 일상 언어
        - "~하지 못했어요" 패턴
        """)

    with col2:
        st.markdown("#### ✂️ 간결성")
        st.markdown("""
        - 1문장 1메시지
        - 제목 20자, 본문 40자 이내
        - 불필요한 수식어 제거
        """)

    with col3:
        st.markdown("#### 🎯 행동 유도")
        st.markdown("""
        - 원인 + 해결 행동 함께 제시
        - "~해 주세요", "~해 보세요"
        - 다음 단계를 명확하게 안내
        """)

    st.markdown("---")

    # ─── 톤 & 보이스 ───
    st.subheader("🗣️ 톤 & 보이스")

    st.markdown("""
    | 항목 | 한컴 스타일 |
    |---|---|
    | **존칭** | ~해요, ~할 수 있어요 (해요체) |
    | **톤** | 친근하지만 신뢰감 있는 |
    | **감정** | 긍정적, 안심시키는 |
    | **주의** | 실패, 불가, 에러, 오류 (부정적 단어) |
    """)

    st.markdown("---")

    # ─── Before/After 예시 ───
    st.subheader("💡 Before / After")

    ex_col1, ex_col2 = st.columns(2)

    with ex_col1:
        st.error("❌ **Before**")
        st.markdown("""
        - "서버 오류가 발생했습니다"
        - "로그인에 실패했습니다"
        - "데이터 없음"
        - "파트너를 모집합니다"
        """)

    with ex_col2:
        st.success("✅ **After**")
        st.markdown("""
        - "문서를 저장하지 못했어요. 잠시 후 다시 시도해 주세요."
        - "로그인하지 못했어요. 비밀번호를 확인해 주세요."
        - "아직 알림이 없어요. 새 소식이 생기면 알려드릴게요."
        - "파트너를 초대합니다"
        """)

    st.markdown("---")

    # ─── 적용 범위 ───
    st.subheader("🌐 적용 서비스")

    st.markdown("""
    | 서비스 | 적용 영역 |
    |---|---|
    | 한컴독스 | UI 문구, 오류 메시지, 온보딩, 릴리즈 노트 |
    | 한컴어시스턴트 | 대화형 응답, 안내 메시지 |
    | 한컴폼즈 | 폼 안내 문구, Empty State |
    | 한컴닷컴 | 마케팅 카피, 서비스 소개, 배너 |
    | 한컴오피스 | 메뉴, 도움말, 오류 메시지 |
    | 한컴계정 | 인증, 약관, 개인정보 관련 문구 |
    """)

    st.markdown("---")

    # ─── 참조 문서 링크 ───
    st.subheader("📚 참조 문서")

    st.markdown("""
    - [한컴 UX 라이팅 철학 & 원칙](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2064974660)
    - [AI 기반 UX 라이팅 운영 체계](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2065302192)
    - [한컴 서비스 UX 라이팅 거버넌스](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2065367194)
    - [UX 라이팅 레거시 분석 (2023~2025)](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/1993508026)
    - [Claude 역추론 규칙서 및 용어집](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2049343956)
    """)

    st.info("👈 **용어집 검색**은 '📖 용어집' 탭에서, **Best/Worst 사례**는 '✅ Best/Worst 사례' 탭에서 확인하세요.")


# ════════════════════════════════════════
# 탭 2: 용어집
# ════════════════════════════════════════
with tab2:
    st.header("📖 용어집 검색")
    st.caption("표준 용어, 주의 표현, 영문 대응어를 검색하세요.")

    # 검색 + 필터
    filter_col, search_col = st.columns([1, 4])
    with filter_col:
        categories = ["전체"] + sorted(set(t.get("category", "일반") for t in terms_db))
        term_category = st.selectbox("카테고리", categories)
    with search_col:
        term_query = st.text_input(
            "용어 검색",
            placeholder="예: 비밀번호, 로그인, 삭제, password"
        )


    # 필터링
    filtered_terms = terms_db

    if term_category != "전체":
        filtered_terms = [t for t in filtered_terms if t.get("category", "일반") == term_category]

    if term_query:
        query_lower = term_query.lower()
        scored_terms = []
        for t in filtered_terms:
            score = 0
            # 표준어 매칭 (가장 높은 점수)
            if query_lower in t["standard"].lower():
                score += 10
            # 주의어 매칭
            for f in t.get("forbidden", []):
                if query_lower in f.lower():
                    score += 5
            # 영문 매칭
            if query_lower in t.get("english", "").lower():
                score += 5
            # 참고사항 매칭
            if query_lower in t.get("note", "").lower():
                score += 2
            if score > 0:
                scored_terms.append((score, t))

        scored_terms.sort(key=lambda x: x[0], reverse=True)
        filtered_terms = [t for _, t in scored_terms]

    # 결과 표시
    if term_query and not filtered_terms:
        st.warning(f"'{term_query}'에 대한 검색 결과가 없습니다.")
        st.info("💡 관리 탭에서 새 용어를 추가하거나, CSV 파일을 임포트할 수 있습니다.")
    else:
        st.markdown(f"**{len(filtered_terms)}건**의 용어")

        for t in filtered_terms:
            forbidden_str = ", ".join(t.get("forbidden", [])) if t.get("forbidden") else "—"
            with st.expander(f"✅ {t['standard']}  |  🌐 {t.get('english', '—')}  |  🏷️ {t.get('category', '일반')}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**✅ 표준 표현**: {t['standard']}")
                    st.markdown(f"**❌ 주의 표현**: {forbidden_str}")
                    st.markdown(f"**🌐 영문**: {t.get('english', '—')}")
                with col_b:
                    st.markdown(f"**🏷️ 카테고리**: {t.get('category', '일반')}")
                    st.markdown(f"**📌 적용 서비스**: {t.get('service', '전체')}")
                    if t.get("note"):
                        st.markdown(f"**💡 참고**: {t['note']}")


# ════════════════════════════════════════
# 탭 3: Best/Worst 사례
# ════════════════════════════════════════
with tab3:
    st.header("✅ Best/Worst 사례")
    st.caption("맥락별로 '이렇게 쓰지 마세요 / 이렇게 쓰세요' 사례를 검색하세요.")

    # 필터 + 검색
    sample_col1, sample_col2 = st.columns([1, 3])
    with sample_col1:
        sample_contexts = ["전체"] + sorted(set(s["context"] for s in samples_db))
        sample_filter = st.selectbox("맥락 필터", sample_contexts)
    with sample_col2:
        sample_query = st.text_input(
            "사례 검색",
            placeholder="예: 저장, 로그인, 삭제, 알림"
        )

    # 필터링
    filtered_samples = samples_db

    if sample_filter != "전체":
        filtered_samples = [s for s in filtered_samples if s["context"] == sample_filter]

    if sample_query:
        query_lower = sample_query.lower()
        filtered_samples = [
            s for s in filtered_samples
            if query_lower in s["worst"].lower()
            or query_lower in s["best"].lower()
            or query_lower in s.get("principle", "").lower()
            or query_lower in s.get("context", "").lower()
        ]

    # 통계
    if filtered_samples:
        st.markdown(f"**{len(filtered_samples)}건**의 사례")

        for s in filtered_samples:
            context_emoji = {
                "오류": "🔴", "Empty State": "⬜", "과금": "💰",
                "마케팅": "📢", "릴리즈 노트": "📋", "온보딩": "👋",
                "삭제/탈퇴": "⚠️", "용어": "📖", "접근성": "♿",
                "법률/약관": "⚖️"
            }.get(s["context"], "📝")

            with st.expander(f"{context_emoji} {s['id']} — ❌ {s['worst'][:40]}..."):
                col_w, col_b = st.columns(2)
                with col_w:
                    st.markdown("#### ❌ Worst")
                    st.error(s["worst"])
                with col_b:
                    st.markdown("#### ✅ Best")
                    st.success(s["best"])

                st.markdown(f"**📌 적용 원칙**: {s['principle']}")
                st.markdown(f"**🏷️ 맥락**: {s['context']}")
                if s.get("source"):
                    st.markdown(f"**📄 출처**: {s['source']}")
    else:
        st.info("조건에 맞는 사례가 없습니다.")

    # 맥락별 통계
    if samples_db:
        st.markdown("---")
        st.markdown("### 📊 맥락별 사례 수")
        context_counts = {}
        for s in samples_db:
            ctx = s["context"]
            context_counts[ctx] = context_counts.get(ctx, 0) + 1

        stat_cols = st.columns(min(len(context_counts), 5))
        for i, (ctx, count) in enumerate(sorted(context_counts.items(), key=lambda x: x[1], reverse=True)):
            with stat_cols[i % len(stat_cols)]:
                st.metric(ctx, f"{count}건")


# ════════════════════════════════════════
# 탭 4: 관리
# ════════════════════════════════════════
with tab4:
    st.header("⚙️ 데이터 관리")

    mgmt_tab1, mgmt_tab2, mgmt_tab3, mgmt_tab4 = st.tabs([
        "📥 CSV 임포트", "➕ 용어 추가", "➕ 사례 추가", "📤 내보내기"
    ])

    # ─── CSV 임포트 ───
    with mgmt_tab1:
        st.subheader("📥 CSV 임포트 (용어집)")
        st.markdown("""
        **CSV 형식 안내:**
        
        | 열 이름 | 필수 | 설명 | 예시 |
        |---|---|---|---|
        | `standard` | ✅ | 표준 표현 | 비밀번호 |
        | `forbidden` | | 주의 표현 (쉼표 구분) | 암호, 패스워드 |
        | `english` | | 영문 대응어 | Password |
        | `category` | | 카테고리 | 인증 |
        | `service` | | 적용 서비스 | 전체 |
        | `note` | | 참고사항 | 기존→현재 |
        
        💡 **한컴_용어집.csv를 그대로 업로드하면 자동 변환됩니다.**
        """)

        uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

        if uploaded_file:
            try:
                # CSV 읽기 (다양한 인코딩 시도)
                content = uploaded_file.read()
                for encoding in ["utf-8-sig", "utf-8", "cp949", "euc-kr"]:
                    try:
                        text = content.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue

                reader = csv.DictReader(io.StringIO(text))
                new_terms = []
                for row in reader:
                    term = {
                        "standard": row.get("standard", row.get("표준", "")).strip(),
                        "forbidden": [
                            f.strip()
                            for f in row.get("forbidden", row.get("주의", "")).split(",")
                            if f.strip()
                        ],
                        "english": row.get("english", row.get("영문", "")).strip(),
                        "category": row.get("category", row.get("카테고리", "일반")).strip(),
                        "service": row.get("service", row.get("서비스", "전체")).strip(),
                        "note": row.get("note", row.get("참고", "")).strip()
                    }
                    if term["standard"]:
                        new_terms.append(term)

                if new_terms:
                    st.success(f"✅ {len(new_terms)}건의 용어를 발견했습니다.")

                    # 미리보기
                    with st.expander("미리보기 (처음 5건)"):
                        for t in new_terms[:5]:
                            st.markdown(f"- **{t['standard']}** → 주의: {', '.join(t['forbidden'])} | 영문: {t['english']}")

                    # 중복 체크
                    existing_standards = {t["standard"] for t in terms_db}
                    duplicates = [t for t in new_terms if t["standard"] in existing_standards]
                    new_only = [t for t in new_terms if t["standard"] not in existing_standards]

                    if duplicates:
                        st.warning(f"⚠️ {len(duplicates)}건은 이미 존재합니다: {', '.join(t['standard'] for t in duplicates[:5])}")

                    import_mode = st.radio(
                        "임포트 방식",
                        ["새 용어만 추가 (중복 건너뛰기)", "전체 덮어쓰기 (기존 데이터 교체)", "전부 추가 (중복 허용)"]
                    )

                    if st.button("📥 임포트 실행", type="primary"):
                        if import_mode == "새 용어만 추가 (중복 건너뛰기)":
                            terms_db.extend(new_only)
                            save_terms(terms_db)
                            st.success(f"✅ {len(new_only)}건 추가 완료! (중복 {len(duplicates)}건 건너뜀)")
                        elif import_mode == "전체 덮어쓰기 (기존 데이터 교체)":
                            save_terms(new_terms)
                            st.success(f"✅ {len(new_terms)}건으로 교체 완료!")
                        else:
                            terms_db.extend(new_terms)
                            save_terms(terms_db)
                            st.success(f"✅ {len(new_terms)}건 추가 완료!")
                        st.rerun()
                else:
                    st.warning("CSV에서 유효한 용어를 찾지 못했습니다. 열 이름을 확인해 주세요.")

            except Exception as e:
                st.error(f"CSV 파일 처리 중 오류: {e}")

    # ─── 용어 추가 ───
    with mgmt_tab2:
        st.subheader("➕ 새 용어 추가")

        with st.form("add_term_form"):
            new_standard = st.text_input("표준 표현 *", placeholder="예: 비밀번호")
            new_forbidden = st.text_input("주의 표현 (쉼표로 구분)", placeholder="예: 암호, 패스워드, password")
            new_english = st.text_input("영문 대응어", placeholder="예: Password")

            add_col1, add_col2 = st.columns(2)
            with add_col1:
                new_category = st.selectbox(
                    "카테고리",
                    ["인증", "UI 공통", "문서", "과금", "계정", "시스템", "접근성", "법률", "마케팅", "일반"]
                )
            with add_col2:
                new_service = st.selectbox(
                    "적용 서비스",
                    ["전체", "한컴독스", "한컴어시스턴트", "한컴폼즈", "한컴닷컴", "한컴오피스", "한컴계정"]
                )

            new_note = st.text_input("참고사항", placeholder="예: '기존 비밀번호' → '현재 비밀번호'로 변경")

            submitted = st.form_submit_button("➕ 추가", type="primary", use_container_width=True)

            if submitted:
                if not new_standard.strip():
                    st.warning("표준 표현은 필수입니다.")
                else:
                    new_term = {
                        "standard": new_standard.strip(),
                        "forbidden": [f.strip() for f in new_forbidden.split(",") if f.strip()],
                        "english": new_english.strip(),
                        "category": new_category,
                        "service": new_service,
                        "note": new_note.strip()
                    }
                    terms_db.append(new_term)
                    save_terms(terms_db)
                    st.success(f"✅ '{new_standard}' 추가 완료!")
                    st.rerun()

    # ─── 사례 추가 ───
    with mgmt_tab3:
        st.subheader("➕ 새 Best/Worst 사례 추가")

        with st.form("add_sample_form"):
            # ID 자동 생성
            context_prefix = {
                "오류": "ERR", "Empty State": "EMP", "과금": "PAY",
                "마케팅": "BRD", "릴리즈 노트": "REL", "온보딩": "ONBD",
                "삭제/탈퇴": "DEL", "용어": "TRM", "접근성": "ACC",
                "법률/약관": "LAW"
            }

            sample_context = st.selectbox(
                "맥락 *",
                list(context_prefix.keys())
            )

            # 해당 맥락의 기존 사례 수로 ID 생성
            existing_count = len([s for s in samples_db if s["context"] == sample_context])
            auto_id = f"{context_prefix[sample_context]}-{existing_count + 1:03d}"
            st.text_input("ID (자동 생성)", value=auto_id, disabled=True)

            sample_worst = st.text_area("❌ Worst 문구 *", placeholder="예: 서버 오류가 발생했습니다")
            sample_best = st.text_area("✅ Best 문구 *", placeholder="예: 문서를 저장하지 못했어요. 잠시 후 다시 시도해 주세요.")
            sample_principle = st.text_input("적용 원칙", placeholder="예: 사람 중심 + 행동 제시")
            sample_source = st.text_input("출처", placeholder="예: UX 라이팅 철학 & 원칙")

            sample_submitted = st.form_submit_button("➕ 추가", type="primary", use_container_width=True)

            if sample_submitted:
                if not sample_worst.strip() or not sample_best.strip():
                    st.warning("Worst와 Best 문구는 필수입니다.")
                else:
                    new_sample = {
                        "id": auto_id,
                        "context": sample_context,
                        "worst": sample_worst.strip(),
                        "best": sample_best.strip(),
                        "principle": sample_principle.strip(),
                        "source": sample_source.strip()
                    }
                    samples_db.append(new_sample)
                    save_samples(samples_db)
                    st.success(f"✅ {auto_id} 추가 완료!")
                    st.rerun()

    # ─── 내보내기 ───
    with mgmt_tab4:
        st.subheader("📤 데이터 내보내기")

        export_col1, export_col2, export_col3 = st.columns(3)

        with export_col1:
            st.markdown("**용어집**")
            if terms_db:
                # JSON
                st.download_button(
                    "📥 JSON 다운로드",
                    json.dumps(terms_db, ensure_ascii=False, indent=2),
                    file_name=f"terms_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                # CSV
                csv_buffer = io.StringIO()
                writer = csv.DictWriter(csv_buffer, fieldnames=["standard", "forbidden", "english", "category", "service", "note"])
                writer.writeheader()
                for t in terms_db:
                    row = t.copy()
                    row["forbidden"] = ", ".join(row.get("forbidden", []))
                    writer.writerow(row)
                st.download_button(
                    "📥 CSV 다운로드",
                    csv_buffer.getvalue(),
                    file_name=f"terms_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                st.caption(f"총 {len(terms_db)}건")

        with export_col2:
            st.markdown("**Best/Worst 사례**")
            if samples_db:
                st.download_button(
                    "📥 JSON 다운로드",
                    json.dumps(samples_db, ensure_ascii=False, indent=2),
                    file_name=f"samples_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                csv_buffer2 = io.StringIO()
                writer2 = csv.DictWriter(csv_buffer2, fieldnames=["id", "context", "worst", "best", "principle", "source"])
                writer2.writeheader()
                for s in samples_db:
                    writer2.writerow(s)
                st.download_button(
                    "📥 CSV 다운로드",
                    csv_buffer2.getvalue(),
                    file_name=f"samples_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                st.caption(f"총 {len(samples_db)}건")

        with export_col3:
            st.markdown("**프롬프트 템플릿**")
            if prompts_db:
                st.download_button(
                    "📥 JSON 다운로드",
                    json.dumps(prompts_db, ensure_ascii=False, indent=2),
                    file_name=f"prompts_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                st.caption(f"총 {len(prompts_db)}건")


# ─── 하단 참조 ───
st.markdown("---")
st.markdown("""
**참조 문서** |
[UX 라이팅 철학 & 원칙](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2064974660) |
[AI 기반 UX 라이팅 운영 체계](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2065302192) |
[Claude 역추론 규칙서 및 용어집](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2049343956) |
[UX 라이팅 거버넌스](https://hancom.atlassian.net/wiki/spaces/MALCOMMON/pages/2065367194)
""")
