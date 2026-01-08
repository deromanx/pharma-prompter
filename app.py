import streamlit as st

# --- 1. 頁面全域設定 ---
st.set_page_config(page_title="Pharma Visual Prompter", page_icon="💊", layout="wide")

# --- 2. 質感設計 (CSS Injection) ---
# 這裡使用 HTML/CSS 來調整標題樣式，隱藏預設醜醜的選單，提升質感
st.markdown("""
<style>
    /* 標題樣式 */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 0px;
    }
    .version-tag {
        font-size: 1rem;
        color: #95A5A6;
        font-weight: 400;
        vertical-align: super;
    }
    .sub-title {
        text-align: center;
        color: #7F8C8D;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    /* 按鈕樣式 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        background-color: #2980B9; /* 專業藍 */
        color: white;
    }
    /* 輸入框優化 */
    .stTextArea textarea {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 標題區 (使用自訂 HTML) ---
st.markdown('<div class="main-title">Pharma Visual Prompter <span class="version-tag">v4.0</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">醫藥行銷專用 AI 指令生成器 | 台灣在地化版 🇹🇼</div>', unsafe_allow_html=True)

# --- 4. 側邊欄：結構設定 ---
with st.sidebar:
    st.header("⚙️ 參數設定")
    
    # 場景選擇
    scenario = st.selectbox(
        "行銷場景 (Scenario)",
        ["民眾衛教 (Public Awareness)", "醫護專業溝通 (HCP Professional)", "品牌形象 (Brand Image)", "患者旅程 (Patient Journey)"]
    )

    # 風格選擇
    style = st.selectbox(
        "藝術風格 (Art Style)",
        ["寫實攝影 (Photorealistic)", "3D 醫療渲染 (3D Render)", "溫暖手繪風 (Warm Illustration)", "極簡資訊圖表 (Infographic)"]
    )
    
    # 比例選擇
    ar_label = st.selectbox(
        "圖片比例 (Aspect Ratio)",
        ["橫式 16:9 (簡報/影片)", "直式 9:16 (IG Reels/限動)", "正方形 1:1 (社群貼文)", "寬扁型 20:9 (網站 Banner)"]
    )
    
    ar_map = {
        "橫式 16:9 (簡報/影片)": "--ar 16:9",
        "直式 9:16 (IG Reels/限動)": "--ar 9:16",
        "正方形 1:1 (社群貼文)": "--ar 1:1",
        "寬扁型 20:9 (網站 Banner)": "--ar 20:9"
    }
    
    st.markdown("---")
    # 法規開關 (預設開啟)
    compliance_check = st.checkbox("✅ 啟用 Compliance 防護 (排除血腥/變形)", value=True)
    negative_prompt = "--no blood, gore, scary, deformity, extra fingers, text, watermark, pills spilling, messy background"

# --- 5. 主操作區 ---
# 使用 container 增加版面層次感
with st.container():
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("1. 畫面主體描述")
        main_subject = st.text_area(
            "請描述畫面內容 (Subject)", 
            height=150, 
            placeholder="例如：一位年輕的藥師正在向老年患者解釋用藥，場景在明亮的社區藥局，氣氛親切..."
        )

    with col2:
        st.subheader("2. 氛圍定調")
        
        # 改為選單式，不再手動輸入
        color_theme = st.selectbox(
            "選擇色調與氣氛 (Color & Mood)",
            [
                "🏥 專業信任 (Medical Blue & White) - 適合醫師溝通",
                "☀️ 溫暖療癒 (Warm Orange & Sunlight) - 適合衛教/家庭",
                "🌿 自然清新 (Green & Clean Nature) - 適合預防醫學",
                "🧬 科技未來 (Silver & Neon Cyan) - 適合新機轉/研討會",
                "🛡️ 警示防護 (Red & Gold) - 適合強調風險或保護",
                "🌫️ 柔和低飽和 (Muted Pastel) - 適合女性/兒童議題"
            ]
        )
        
        # 顯示當前設定摘要
        st.info(f"📍 自動鎖定：台灣面孔 (Taiwanese/Asian)")

# --- 6. 核心生成邏輯 ---
if st.button("✨ 生成 Prompt", type="primary"):
    if not main_subject:
        st.error("請先輸入畫面描述！")
    else:
        # 1. 處理色調字串 (去除前面的 emoji 和說明，只留括號內的英文)
        # 例如取 "Medical Blue & White"
        import re
        color_keywords = re.search(r'\((.*?)\)', color_theme).group(1)

        # 2. 設定場景魔法詞 (Magic Words)
        if "衛教" in scenario or "患者" in scenario:
            magic_words = "lifestyle photography, natural lighting, candid moment, high quality"
        elif "醫護" in scenario:
            magic_words = "clinical accuracy, professional atmosphere, macro details, depth of field"
        elif "品牌" in scenario:
            magic_words = "cinematic lighting, abstract concept, award winning photography, 8k"
        else:
            magic_words = "high quality, sharp focus"

        # 3. 🇹🇼 在地化鎖定 (Localization Lock)
        # 這是關鍵：強制加入台灣/亞洲特徵
        localization_keywords = "Taiwanese people, East Asian ethnicity, modern Taipei city vibe, asian features"

        # 4. 組合最終指令
        # 結構：Subject + Context + Style + Color + Localization + Tech Specs
        final_prompt = (
            f"/imagine prompt: "
            f"**Subject:** {main_subject}. "
            f"**Context:** {scenario}. "
            f"**Style:** {style}. "
            f"**Atmosphere:** {color_keywords}. "
            f"**Character:** {localization_keywords}. "  # 強制插入
            f"**Tech Specs:** {magic_words} "
            f"{ar_map[ar_label]} --v 6.0 --stylize 250"
        )
        
        if compliance_check:
            final_prompt += f" {negative_prompt}"

        # --- 7. 結果呈現 ---
        st.divider()
        st.success("🎉 Prompt 已生成！(已優化為台灣風格)")
        st.code(final_prompt, language="markdown")
        
        # 預覽提示
        st.caption("💡 小撇步：這段指令已包含 `Taiwanese people` 參數，Midjourney 產出的人物將會非常符合台灣在地情境。")