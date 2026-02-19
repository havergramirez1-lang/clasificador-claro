import streamlit as st
import google.generativeai as genai
import json

# --- CONFIGURACIÓN DE LA IA (Versión Ultra-Compatible) ---
API_KEY = "AIzaSyAqJ0V6oePMCvjmuUHii_YM1FQ2qBHMolA"

# Configuramos la conexión forzando la versión estable 'v1'
genai.configure(api_key=API_KEY, transport='rest')

# Definimos el modelo asegurando la compatibilidad
# Definimos el modelo de forma simple y directa
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash'
)

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Asistente Front Claro", page_icon="📡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #ef3340; color: white; border-radius: 10px; }
    .result-card { padding: 20px; border-radius: 15px; border-left: 10px solid #ef3340; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Clasificador Inteligente de Casos - Front CLARO")
st.info("Pega la descripción del requerimiento del cliente para determinar el escalamiento.")

# --- INTERFAZ DE USUARIO ---
col1, col2 = st.columns([1, 1])

with col1:
    descripcion = st.text_area("Descripción del Requerimiento / Solicitud del Cliente:", height=300, 
                                placeholder="Ejemplo: Cliente reporta lentitud en el servicio SDWAN y requiere revisión de enlaces...")
    btn_analizar = st.button("ANALIZAR CASO")

with col2:
    if btn_analizar and descripcion:
        with st.spinner('Analizando con IA...'):
            # El Prompt con tus reglas de negocio
            prompt = f"""
            Eres un experto en soporte Front de CLARO Colombia. Tu tarea es clasificar solicitudes.
            
            REGLAS DE ASIGNACIÓN:
            1. 'EYN - NOC Corporativo' (Tipo IM): Fallas, lentitud, intermitencia, caídas de servicio, problemas de voz/conectividad.
            2. 'EYN - Cambios Configuracion' (Tipo CI): NAT, VLAN, DHCP, Firewall, Enrutamiento (BGP/Estático), SNMP, Syslog, nuevas interfaces.
            3. 'EYN - Soporte Empresas IRE' (Tipo RF): Pruebas de conmutación, consultas técnicas, recuperar gestión, certificaciones.

            PRIORIDAD:
            - ALTA: Caídas totales o afectación crítica.
            - MEDIA: Lentitud, intermitencias, cambios (CI) y requerimientos (RF).
            - BAJA: Consultas informativas.

            TEXTO A ANALIZAR: "{descripcion}"

            RESPONDE ÚNICAMENTE EN FORMATO JSON:
            {{
                "area": "Nombre del Area",
                "tipo": "IM o CI o RF",
                "prioridad": "ALTA o MEDIA o BAJA",
                "justificacion": "Breve explicación técnica"
            }}
            """
            
            try:
                response = model.generate_content(prompt)
                # Limpiar la respuesta para asegurar que sea JSON puro
                res_text = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(res_text)

                # Mostrar Resultados Visuales
                st.markdown(f"""
                <div class="result-card">
                    <h3>🎯 Resultado del Análisis</h3>
                    <p><b>Área de Destino:</b> {data['area']}</p>
                    <p><b>Tipo de Ticket:</b> <span style='color:red; font-weight:bold;'>{data['tipo']}</span></p>
                    <p><b>Prioridad Sugerida:</b> {data['prioridad']}</p>
                    <hr>
                    <p><b>Justificación:</b> {data['justificacion']}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error al procesar: {e}")
    elif btn_analizar:
        st.warning("Por favor, ingresa una descripción para continuar.")
