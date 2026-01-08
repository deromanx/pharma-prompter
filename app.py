import streamlit as st

# --- 頁面設定 ---
st.set_page_config(page_title="醫藥行銷視覺生成器 v2.0", page_icon="💊", layout="wide")

st.title("💊 Pharma Visual Prompter v2.0")
st.markdown("---")

# --- 側邊欄：進階參數設定 ---
with st.sidebar:
    st.header("🎨 視覺參數面板")
    
    # 1. 行銷場景 (更新版)
    scenario = st.selectbox(
        "行銷場景 (Scenario)",
        ["民眾衛教 (Public Education)", 
         "醫療人員專業溝通 (HCP Communication)", 
         "品牌形象 (Brand Image)"]
    )

    # 2. 藝術風格
    style = st.selectbox(
        "藝術風格 (Art Style)",
        ["寫實攝影 (Photorealistic)", 
         "3D 醫療渲染 (3D Medical Render)", 
         "極簡向量圖 (Minimalist Vector)", 
         "溫暖插畫風 (Warm Illustration)"]
    )
    
    # 3. 圖片比例 (新增特殊比例)
    ar_label = st.selectbox(
        "圖片比例 (Aspect Ratio)",
        ["橫式 16:9 (簡報/影片)", 
         "直式 9:16 (IG Reels/限動)", 
         "正方形 1:1 (FB/IG 貼文)", 
         "細長型 9:20 (手機滿版活動頁)", 
         "寬扁型 20:9 (網站 Banner header)"]
    )
    
    # 建立比例對照表 (Mapping)
    ar_map = {
        "橫式 16:9 (簡報/影片)": "--ar 16:9",
        "直式 9:16 (IG Reels/限動)": "--ar 9:16",
        "正方形 1:1 (FB/IG 貼文)": "--ar 1:1",
        "細長型 9:20 (手機滿版活動頁)": "--ar 9:20",
        "寬扁型 20:9 (網站 Banner header)": "--ar 20:9"
    }

# --- 主畫面：輸入區 ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1. 描述您的畫面")
    main_subject = st.text_area("主體描述 (Subject)", height=100, placeholder="例如：一位專業醫師正在向患者解釋病情，手持平板電腦，光線明亮專業...")
    
with col2:
    st.subheader("2. 設定氛圍")
    color_tone = st.text_input("色調與氣氛", placeholder="例如：醫療藍、信任感、科技銀")
    lighting = st.text_input("光影設定", placeholder="例如：自然光、手術室聚光、柔和晨光", value="Professional studio lighting")

# --- 核心邏輯：Prompt 組合 ---
if st.button("✨ 生成高階指令 (Generate Prompt)", type="primary"):
    
    # 根據新場景設定「魔法詞」(Magic Words)
    magic_words = ""
    
    if "民眾衛教" in scenario:
        # 衛教：強調親切、易懂、不可怕
        magic_words = "friendly, easy to understand infographic style, warm atmosphere, hopeful, educational, clean composition"
    elif "醫療人員" in scenario:
        # HCP：強調科學、精確、微距、高細節
        magic_words = "scientific visualization, mode of action (MOA), molecular detail, macro photography, clinical accuracy, unreal engine 5 render, hyper-detailed"
    elif "品牌形象" in scenario:
        # 品牌：強調大氣、抽象、高級感
        magic_words = "cinematic lighting, award-winning photography, emotional connection, high-end, abstract concept, depth of field, 8k resolution"

    # 組合最終指令
    final_prompt = f"/imagine prompt: **Subject:** {main_subject}. **Context:** {scenario}. **Style:** {style}. **Atmosphere:** {color_tone}, {lighting}. **Tech Specs:** {magic_words} {ar_map[ar_label]} --v 6.0 --stylize 250"

    # --- 顯示結果區域 ---
    st.divider()
    st.success("🎉 指令已生成！請複製下方文字：")
    
    # 使用 code block 方便複製
    st.code(final_prompt, language="markdown")
    
    # 顯示參數解析 (讓您確認 AI 加了什麼料)
    with st.expander("查看 AI 自動加入的參數細節"):
        st.write(f"🔹 **選定場景：** {scenario}")
        st.write(f"🔹 **自動加入魔法詞：** `{magic_words}`")
        st.write(f"🔹 **比例參數：** `{ar_map[ar_label]}`")