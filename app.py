import streamlit as st

# --- 1. 頁面全域設定 ---
st.set_page_config(page_title="Pharma Visual Prompter v5.0", page_icon="💊", layout="wide")

# --- 2. 質感設計 (CSS Injection) ---
st.markdown("""
<style>
    /* 標題樣式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2C3E50;
        text-align: center;
        margin-top: -20px;
    }
    .version-tag {
        font-size: 0.8rem;
        color: white;
        background-color: #E74C3C;
        padding: 2px 8px;
        border-radius: 10px;
        vertical-align: middle;
        margin-left: 10px;
    }
    .sub-title {
        text-align: center;
        color: #7F8C8D;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    /* 區塊背景優化 */
    .stSelectbox, .stTextInput {
        margin-bottom: 0.5rem;
    }
    /* 按鈕樣式 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        font-size: 1.2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #2980B9 0%, #6DD5FA 100%);
        color: white;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 標題區 ---
st.markdown('<div class="main-title">Pharma Visual Prompter <span class="version-tag">v5.0</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">醫藥行銷 AI 產圖指令生成器</div>', unsafe_allow_html=True)

st.markdown("---")

# --- 4. 上半部：參數設定儀表板 (Dashboard) ---
# 使用 container 包住，增加結構感
with st.container():
    st.subheader("🛠️ 參數設定 (Settings)")
    
    # 第一排：三個主要參數 (3欄位)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scenario = st.selectbox(
            "1. 行銷場景 (Scenario)",
            ["民眾衛教 (Public Awareness)", "醫護專業溝通 (HCP Professional)", "品牌形象 (Brand Image)", "患者旅程 (Patient Journey)"]
        )
    with col2:
        style = st.selectbox(
            "2. 藝術風格 (Style)",
            ["寫實攝影 (Photorealistic)", "3D 醫療渲染 (3D Render)", "溫暖手繪風 (Warm Illustration)", "極簡資訊圖表 (Infographic)"]
        )
    with col3:
        ar_label = st.selectbox(
            "3. 圖片比例 (Ratio)",
            ["橫式 16:9 (簡報/影片)", "直式 9:16 (IG Reels/限動)", "正方形 1:1 (社群貼文)", "寬扁型 20:9 (網站 Banner)"]
        )

    # 第二排：氛圍與法規 (2欄位 - 左寬右窄)
    col4, col5 = st.columns([2, 1])
    
    with col4:
        color_theme = st.selectbox(
            "4. 氛圍定調 (Atmosphere & Color)",
            [
                "🏥 專業信任 (Medical Blue & White) - 適合醫師溝通",
                "☀️ 溫暖療癒 (Warm Orange & Sunlight) - 適合衛教/家庭",
                "🌿 自然清新 (Green & Clean Nature) - 適合預防醫學",
                "🧬 科技未來 (Silver & Neon Cyan) - 適合新機轉/研討會",
                "🛡️ 警示防護 (Red & Gold) - 適合強調風險或保護",
                "🌫️ 柔和低飽和 (Muted Pastel) - 適合女性/兒童議題"
            ]
        )
    with col5:
        st.write("") # 為了排版對齊的空行
        st.write("") 
        compliance_check = st.checkbox("✅ 啟用法規防護", value=True, help="自動排除血腥、變形、恐怖元素")

# --- 5. 下半部：畫面描述 (Main Input) ---
st.markdown("---")
with st.container():
    st.subheader("📝 畫面主體描述 (Prompt Input)")
    
    main_subject = st.text_area(
        "請在此輸入畫面內容，AI 將自動轉化為高品質指令...", 
        height=150, 
        placeholder="💡 範例：一位年輕的藥師正在向老年患者解釋用藥，場景在明亮的社區藥局，兩人微笑互動，展現專業與關懷..."
    )

    # 參數對照表
    ar_map = {
        "橫式 16:9 (簡報/影片)": "--ar 16:9",
        "直式 9:16 (IG Reels/限動)": "--ar 9:16",
        "正方形 1:1 (社群貼文)": "--ar 1:1",
        "寬扁型 20:9 (網站 Banner)": "--ar 20:9"
    }
    negative_prompt = "--no blood, gore, scary, deformity, extra fingers, text, watermark, pills spilling, messy background, ugly face"

# --- 6. 生成按鈕與邏輯 ---
st.markdown("<br>", unsafe_allow_html=True) # 增加一點間距

if st.button("🚀 生成 AI 指令 (Generate Prompt)"):
    if not main_subject:
        st.warning("⚠️ 請記得輸入畫面描述喔！")
    else:
        # 解析顏色
        import re
        color_keywords = re.search(r'\((.*?)\)', color_theme).group(1)

        # 設定 Magic Words
        if "衛教" in scenario or "患者" in scenario:
            magic_words = "lifestyle photography, natural lighting, candid moment, high quality, 8k"
        elif "醫護" in scenario:
            magic_words = "clinical accuracy, professional atmosphere, macro details, depth of field, sharp focus"
        elif "品牌" in scenario:
            magic_words = "cinematic lighting, abstract concept, award winning photography, advertisement quality"
        else:
            magic_words = "high quality, sharp focus"

        # 在地化鎖定 (台灣)
        localization = "Taiwanese people, East Asian ethnicity, modern Taipei city vibe, asian features"

        # 組合 Prompt
        final_prompt = (
            f"/imagine prompt: "
            f"**Subject:** {main_subject}. "
            f"**Context:** {scenario}. "
            f"**Style:** {style}. "
            f"**Atmosphere:** {color_keywords}. "
            f"**Character:** {localization}. " 
            f"**Tech Specs:** {magic_words} "
            f"{ar_map[ar_label]} --v 6.0 --stylize 250"
        )
        
        if compliance_check:
            final_prompt += f" {negative_prompt}"

        # 顯示結果
        st.success("✨ 指令生成成功！")
        st.code(final_prompt, language="markdown")
        
        # 顯示當前設定標籤 (確認用)
        st.caption(f"📍 設定確認：{scenario.split(' ')[0]} | {style.split(' ')[0]} | {ar_label.split(' ')[0]} | 台灣風格鎖定")