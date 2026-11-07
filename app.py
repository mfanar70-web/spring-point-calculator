import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Spring Calculator | محاسبات نقاط فنرپیچی",
    page_icon="🌀",
    layout="centered",
)

# ---------- Header ----------
logo_path = Path(__file__).parent / "logo.png"
col_logo, col_title = st.columns([1, 4], vertical_alignment="center")
with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=105)
with col_title:
    st.title("محاسبات نقاط فنرپیچی")
    st.caption("Spring Coiling Point Calculator")

st.divider()

st.markdown(
    """
    این ابزار نقاط میانی را بین حد پایین و حد بالای قطر محاسبه می‌کند.
    **تعداد نقاط شامل نقطه ابتدا و انتها است.**
    """
)

# ---------- Inputs ----------
st.subheader("اطلاعات ورودی")
c1, c2 = st.columns(2)
with c1:
    upper = st.number_input(
        "حد بالای قطر (mm)",
        min_value=0.0,
        value=120.0,
        step=1.0,
        format="%.3f",
    )
with c2:
    lower = st.number_input(
        "حد پایین قطر (mm)",
        min_value=0.0,
        value=40.0,
        step=1.0,
        format="%.3f",
    )

count = st.number_input(
    "تعداد نقاط (با احتساب ابتدا و انتها)",
    min_value=2,
    max_value=500,
    value=5,
    step=1,
)

# ---------- Calculation ----------
if upper <= lower:
    st.error("حد بالای قطر باید از حد پایین قطر بزرگ‌تر باشد.")
else:
    step = (upper - lower) / (int(count) - 1)
    values = [lower + i * step for i in range(int(count))]
    values[-1] = upper  # avoid floating-point display drift

    df = pd.DataFrame({
        "شماره نقطه": range(1, int(count) + 1),
        "قطر (mm)": [round(v, 3) for v in values],
    })

    st.divider()
    st.subheader("نتایج محاسبه")
    st.metric("فاصله یکنواخت بین نقاط", f"{step:.3f} mm")
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="دانلود خروجی Excel-compatible (CSV)",
        data=csv_data,
        file_name="spring_coiling_points.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.subheader("نمودار تغییر قطر")
    fig, ax = plt.subplots()
    ax.plot(df["شماره نقطه"], df["قطر (mm)"], marker="o")
    ax.set_xlabel("Point number")
    ax.set_ylabel("Diameter (mm)")
    ax.set_xticks(df["شماره نقطه"])
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.divider()
st.caption("نسخه اولیه محاسباتی — پیش از استفاده در برنامه دستگاه، ترتیب نقاط و تعریف قطر را با دستورالعمل همان دستگاه تطبیق دهید.")
