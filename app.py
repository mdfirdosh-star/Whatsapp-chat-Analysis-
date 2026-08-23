import streamlit as st
import zipfile

from preprocessing import preprocess
from helper import (
    fatch_stats,
    most_busy_users,
    create_wordcolud,
    most_common_word,
    fatch_emojis,
    most_busy_month
)

import matplotlib.pyplot as plt


st.title("Whatsapp Chat Analyzer")
st.sidebar.title("Whatsapp Chat Analyzer")


# =========================================================
# FILE UPLOADER
# =========================================================

uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=["txt", "zip"]
)


# =========================================================
# FILE PROCESSING
# =========================================================

if uploaded_file is not None:

    try:

        # =================================================
        # TXT FILE
        # =================================================

        if uploaded_file.name.lower().endswith(".txt"):

            bytes_data = uploaded_file.getvalue()

            data = bytes_data.decode(
                "utf-8",
                errors="replace"
            )


        # =================================================
        # ZIP FILE
        # =================================================

        elif uploaded_file.name.lower().endswith(".zip"):

            with zipfile.ZipFile(
                uploaded_file,
                "r"
            ) as zip_ref:

                # ZIP ke andar files
                files = zip_ref.namelist()

                # TXT files find
                txt_files = [
                    file
                    for file in files
                    if file.lower().endswith(".txt")
                    and not file.endswith("/")
                ]

                if len(txt_files) == 0:

                    st.error(
                        "ZIP ke andar .txt WhatsApp chat nahi mili."
                    )

                    st.stop()

                # First TXT file
                txt_file = txt_files[0]

                st.success(
                    f"Chat file found: {txt_file}"
                )

                # TXT read
                bytes_data = zip_ref.read(
                    txt_file
                )

                # Decode
                data = bytes_data.decode(
                    "utf-8",
                    errors="replace"
                )


        # =================================================
        # PREPROCESS
        # =================================================

        df = preprocess(data)

        st.dataframe(
            df,
            use_container_width=True
        )


        # =================================================
        # USER LIST
        # =================================================

        user_list = df["user"].unique().tolist()

        if "group_notification" in user_list:
            user_list.remove("group_notification")

        user_list.sort()

        user_list.insert(
            0,
            "overall"
        )


        # =================================================
        # SELECT USER
        # =================================================

        select_user = st.sidebar.selectbox(
            "Show analysis wrt",
            user_list
        )


        # =================================================
        # SHOW ANALYSIS
        # =================================================

        if st.sidebar.button(
            "Show Analysis"
        ):

            # =============================================
            # 1. STATISTICS
            # =============================================

            num_message, words, media_files, links = fatch_stats(
                select_user,
                df
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Message")
                st.title(num_message)

            with col2:
                st.header("Total Words")
                st.title(words)

            with col3:
                st.header("Total Media Messages")
                st.title(media_files)

            with col4:
                st.header("Total Links")
                st.title(links)


            # =============================================
            # 2. MOST BUSY USER
            # =============================================

            if select_user == "overall":

                st.title(
                    "Most Busy User"
                )

                x, new_df = most_busy_users(
                    df
                )

                col1, col2 = st.columns(2)

                name = x.index
                counts = x.values

                with col1:

                    fig, ax = plt.subplots()

                    ax.bar(
                        name,
                        counts
                    )

                    plt.xticks(
                        rotation=90
                    )

                    st.pyplot(fig)

                with col2:

                    st.dataframe(
                        new_df
                    )


            # =============================================
            # 3. WORDCLOUD
            # =============================================

            st.title(
                "WordCloud"
            )

            df_wc_d = create_wordcolud(
                select_user,
                df
            )

            fig, ax = plt.subplots(
                figsize=(10, 6)
            )

            ax.imshow(
                df_wc_d
            )

            ax.axis("off")

            st.pyplot(fig)


            # =============================================
            # 4. MOST COMMON WORDS
            # =============================================

            st.title(
                "Most Common Words"
            )

            df_m = most_common_word(
                select_user,
                df
            )

            fig, ax = plt.subplots()

            ax.bar(
                df_m["Most_Common_Word"],
                df_m["No Of Words"]
            )

            plt.xticks(
                rotation=90
            )

            st.pyplot(fig)

            st.title(
                "Most Common Word Dataframe"
            )

            st.dataframe(
                df_m
            )


            # =============================================
            # 5. EMOJIS
            # =============================================

            st.title(
                "Show the Emojis"
            )

            emoji_df = fatch_emojis(
                select_user,
                df
            )

            col1, col2 = st.columns(2)

            with col1:

                st.dataframe(
                    emoji_df,
                    use_container_width=True
                )

            with col2:

                st.header(
                    "Emoji Pie Chart"
                )

                if emoji_df.empty:

                    st.info(
                        "No emojis found for this user."
                    )

                else:

                    top_emoji = emoji_df.head(
                        10
                    )

                    fig, ax = plt.subplots(
                        figsize=(6, 5)
                    )

                    ax.pie(
                        top_emoji["count"].astype(float),
                        labels=top_emoji["emoji"].astype(str),
                        autopct="%1.1f%%"
                    )

                    ax.set_title(
                        "Top 10 Used Emojis"
                    )

                    st.pyplot(fig)

                    plt.close(fig)


            # =============================================
            # 6. MOST BUSY MONTH
            # =============================================

            st.title(
                "Most Busy Month"
            )

            timelines = most_busy_month(
                select_user,
                df
            )

            col1, col2 = st.columns(2)

            with col1:

                st.title(
                    "Most Busy Month Graph"
                )

                fig, ax = plt.subplots()

                ax.plot(
                    timelines["time"],
                    timelines["message"]
                )

                plt.xticks(
                    rotation=90
                )

                st.pyplot(fig)

            with col2:

                st.title(
                    "Most Busy Month Bar Plot"
                )

                fig, ax = plt.subplots()

                ax.bar(
                    timelines["time"],
                    timelines["message"]
                )

                plt.xticks(
                    rotation=90
                )

                st.pyplot(fig)


    except zipfile.BadZipFile:

        st.error(
            "Uploaded ZIP file valid nahi hai."
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )
