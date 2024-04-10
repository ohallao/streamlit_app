import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image


custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

@st.cache_data
def load_data(file_path):
    try:
        data_raw = pd.read_csv(file_path, sep=";")
    except:
        data_raw = pd.read_excel(file_path)
    return data_raw
    

def main():
    st.set_page_config(page_title="Telemarketing analisys",
                       page_icon= r"C:\Users\allan\OneDrive\Área de Trabalho\Python\Data Science\3-Desenvolvimento Modelos com Pandas e Python\Módulo 19 - Streamlit II\streamlit_app\img\telmarketing_icon.png",
                       layout="wide",
                       initial_sidebar_state="expanded"
                       )
    st.write("# Telemarkeng Analisys")
    st.markdown("---")

    image = Image.open(r"C:\Users\allan\OneDrive\Área de Trabalho\Python\Data Science\3-Desenvolvimento Modelos com Pandas e Python\Módulo 19 - Streamlit II\streamlit_app\img\Bank-Branding.jpg")
    st.sidebar.image(image)

    # Data reading
    uploaded_file = st.sidebar.file_uploader("Bank marketing data",
                             type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        bank_raw = load_data(r"C:\Users\allan\OneDrive\Área de Trabalho\Python\Data Science\3-Desenvolvimento Modelos com Pandas e Python\Módulo 19 - Streamlit II\streamlit_app\input\bank-additional-full.csv")
        bank = bank_raw.copy()

    
        with st.sidebar.form(key="my_form"):
            
            st.markdown("## Filtro")

            # Radio Buttons
            graph_type = st.radio("Tipo de gráfico", ("Barra", "Pizza"))
            
            # Dropdown Idade
            st.markdown("#### Filter by Age")
            idade_min, idade_max = int(bank['age'].min()), int(bank['age'].max())
            idades = [idade_min, idade_max]
            age_slider = st.slider(label="age slider",
                                   min_value=idades[0],
                                   max_value=idades[1],
                                   value=idades,
                                   step=1,
                                   label_visibility="hidden"
                                   )
            bank = bank.query("age >= @age_slider[0] & age <= @age_slider[1]")

            
            def create_checkbox(df:pd.DataFrame, col:str):
                items = bank[col].unique().tolist()
                selected_items = items 
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"#### Filter by {col}")
                with col2:
                    check_all = st.checkbox(f"select all {col}")
                    
                if check_all:
                    selected_items = items
                else:
                    selected_items=items[0]
                sbox = st.multiselect(f"{col} list",
                                           items,
                                           selected_items,
                                           )
                df = df.query(f"{col} == @sbox")
                return df

            bank = (create_checkbox(bank, 'job')
                    .pipe(create_checkbox, 'marital')
                    .pipe(create_checkbox, 'default')
                    .pipe(create_checkbox, 'housing')
                    .pipe(create_checkbox, 'loan')
                    .pipe(create_checkbox, 'contact')
                    .pipe(create_checkbox, 'month')
                    .pipe(create_checkbox, 'day_of_week')
                    )



            # if sbox_jobs:
            #     bank = bank.query("job == @sbox_jobs")

            submit_button = st.form_submit_button(label="Aplicar")
                

        # Grafico comparação bruto X filtrado
        bank_target_pct = bank.y.value_counts(normalize=True).to_frame()*100
        bank_target_pct = bank_target_pct.sort_index()

        bank_raw_target_pct = bank_raw.y.value_counts(normalize=True).to_frame()*100
        bank_raw_target_pct = bank_raw_target_pct.sort_index()

        fig, ax = plt.subplots(1, 2, figsize=(5, 3))

        if graph_type == 'Barra':
            sns.barplot(x = bank_raw_target_pct.index,
                        y = 'y',
                        data = bank_raw_target_pct,
                        ax=ax[0]
                        )
            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title("dados brutos",
                            fontweight = 'bold')

            sns.barplot(x = bank_target_pct.index,
                        y = 'y',
                        data = bank_target_pct,
                        ax=ax[1]
                        )
            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title("dados filtrados",
                            fontweight = 'bold')
        else:
            bank_raw_target_pct.plot(kind='pie', autopct='%.2f', y='y', ax=ax[0])
            ax[0].set_title('Dados brutos',
                            fontweight='bold')
            bank_target_pct.plot(kind='pie', autopct='%.2f', y='y', ax=ax[1])
            ax[1].set_title('Dados filtrados',
                            fontweight='bold')
            
            

        #Outputs

        
        st.write('## Tabela filtrada')
        st.write(bank)
        st.download_button(label="Download",
                           data=bank.to_csv(),
                           file_name='downloaded_data.csv',
                           mime='data/output/'
                           )
        st.write('## Proporção de aceite')
        st.pyplot(fig)
    

meu_app = main()
