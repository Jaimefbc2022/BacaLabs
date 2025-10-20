Aquí tienes **hit.py** completo. Pégalo como página de Streamlit y listo.

```python
# hit.py
import time
import pandas as pd
import streamlit as st

st.set_page_config(page_title="HIIT Timer", page_icon="⏱️", layout="wide")

# ------------------------- Helpers & State -------------------------
def _init_state():
    defaults = {
        "hiit_running": False,
        "hiit_paused": False,
        "hiit_round": 1,
        "hiit_step_idx": 0,
        "hiit_phase": "work",  # "work" | "rest"
        "hiit_phase_ends_at": None,
        "hiit_config_locked": False,
        "hiit_rounds": 1,
        "hiit_preset_key": "Custom",
        "hiit_steps_df": pd.DataFrame([
            {"name": "Ejercicio 1", "work_s": 30, "rest_s": 30},
            {"name": "Ejercicio 2", "work_s": 30, "rest_s": 30},
            {"name": "Ejercicio 3", "work_s": 30, "rest_s": 30},
            {"name": "Ejercicio 4", "work_s": 30, "rest_s": 30},
        ]),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _format_mmss(seconds: float) -> str:
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"

def _calc_totals(df: pd.DataFrame, rounds: int) -> tuple[int, int]:
    per_round = int(df["work_s"].fillna(0).sum() + df["rest_s"].fillna(0).sum())
    total = per_round * int(rounds)
    return per_round, total

def _advance_to_next_step(steps: pd.DataFrame, total_rounds: int):
    # Siguiente paso o siguiente ronda
    if st.session_state.hiit_step_idx + 1 < len(steps):
        st.session_state.hiit_step_idx += 1
        st.session_state.hiit_phase = "work"
        next_work = int(steps.iloc[st.session_state.hiit_step_idx]["work_s"])
        st.session_state.hiit_phase_ends_at = time.time() + max(1, next_work)
    else:
        # Fin de la vuelta
        if st.session_state.hiit_round < total_rounds:
            st.session_state.hiit_round += 1
            st.session_state.hiit_step_idx = 0
            st.session_state.hiit_phase = "work"
            next_work = int(steps.iloc[0]["work_s"])
            st.session_state.hiit_phase_ends_at = time.time() + max(1, next_work)
            st.toast(f"Inicio ronda {st.session_state.hiit_round}", icon="🔁")
        else:
            # Fin total
            st.session_state.hiit_running = False
            st.session_state.hiit_paused = False
            st.session_state.hiit_config_locked = False
            st.session_state.hiit_phase_ends_at = None
            st.toast("HIIT completado", icon="✅")

def _advance_phase(steps: pd.DataFrame, total_rounds: int):
    i = st.session_state.hiit_step_idx
    row = steps.iloc[i]
    work_s = int(row["work_s"])
    rest_s = int(row["rest_s"])

    if st.session_state.hiit_phase == "work":
        if rest_s > 0:
            st.session_state.hiit_phase = "rest"
            st.session_state.hiit_phase_ends_at = time.time() + max(1, rest_s)
            st.toast("Descanso", icon="🧘")
        else:
            _advance_to_next_step(steps, total_rounds)
    else:
        st.session_state.hiit_phase = "work"
        _advance_to_next_step(steps, total_rounds)

def _start_session(steps: pd.DataFrame, rounds: int):
    if len(steps) == 0:
        st.warning("Añade al menos un paso.")
        return
    st.session_state.hiit_running = True
    st.session_state.hiit_paused = False
    st.session_state.hiit_config_locked = True
    st.session_state.hiit_rounds = int(rounds)
    # Reset si venimos de stop
    st.session_state.hiit_round = 1
    st.session_state.hiit_step_idx = 0
    st.session_state.hiit_phase = "work"
    current_work = int(steps.iloc[0]["work_s"])
    st.session_state.hiit_phase_ends_at = time.time() + max(1, current_work)
    st.toast("HIIT iniciado", icon="▶️")

def _pause_session():
    st.session_state.hiit_paused = True
    st.toast("Pausa", icon="⏸️")

def _resume_session():
    st.session_state.hiit_paused = False
    # No cambiamos hiit_phase_ends_at. Se recalcula por tick.
    st.toast("Reanudar", icon="⏯️")

def _reset_session():
    st.session_state.hiit_running = False
    st.session_state.hiit_paused = False
    st.session_state.hiit_round = 1
    st.session_state.hiit_step_idx = 0
    st.session_state.hiit_phase = "work"
    st.session_state.hiit_phase_ends_at = None
    st.session_state.hiit_config_locked = False
    st.toast("Reset", icon="⏹️")

# ------------------------- UI -------------------------
_init_state()

tab, = st.tabs(["HIIT"])
with tab:
    st.subheader("Timer HIIT configurable")

    # --------- Presets ----------
    presets = {
        "Custom": None,
        "Tabata 20:10 x 8": pd.DataFrame([{"name": f"Tabata {i+1}", "work_s": 20, "rest_s": 10} for i in range(8)]),
        "30:30 x 6": pd.DataFrame([{"name": f"Ejercicio {i+1}", "work_s": 30, "rest_s": 30} for i in range(6)]),
        "45:15 x 6": pd.DataFrame([{"name": f"Ejercicio {i+1}", "work_s": 45, "rest_s": 15} for i in range(6)]),
        "EMOM 60s x 10": pd.DataFrame([{"name": f"EMOM {i+1}", "work_s": 60, "rest_s": 0} for i in range(10)]),
    }

    top_cols = st.columns([1, 1, 2, 2])
    with top_cols[0]:
        preset = st.selectbox(
            "Preset",
            list(presets.keys()),
            index=list(presets.keys()).index(st.session_state.hiit_preset_key) if st.session_state.hiit_preset_key in presets else 0,
        )
    with top_cols[1]:
        apply = st.button("Aplicar preset", use_container_width=True)
    with top_cols[2]:
        rounds = st.number_input(
            "Rondas",
            min_value=1, max_value=99, value=int(st.session_state.hiit_rounds), step=1,
            disabled=st.session_state.hiit_config_locked
        )
    with top_cols[3]:
        st.caption("Tip: si bloqueas configuración en marcha, evitas cambios accidentales.")

    if apply and preset != "Custom":
        st.session_state.hiit_steps_df = presets[preset].copy()
        st.session_state.hiit_preset_key = preset
        st.rerun()
    elif apply and preset == "Custom":
        st.session_state.hiit_preset_key = "Custom"
        st.rerun()

    # --------- Editor de pasos ----------
    st.caption("Edita los pasos. Tiempos en segundos. Puedes añadir o borrar filas.")
    disabled = st.session_state.hiit_config_locked

    steps = st.data_editor(
        st.session_state.hiit_steps_df,
        num_rows="dynamic",
        use_container_width=True,
        disabled=disabled,
        key="hiit_steps_df",
        column_config={
            "name": st.column_config.TextColumn("Paso", help="Nombre del ejercicio"),
            "work_s": st.column_config.NumberColumn("Trabajo (s)", min_value=0, step=5),
            "rest_s": st.column_config.NumberColumn("Descanso (s)", min_value=0, step=5),
        }
    )

    # --------- Resumen ----------
    if len(steps) > 0:
        per_round, total_est = _calc_totals(steps, rounds)
        st.info(f"Tiempo por ronda: {_format_mmss(per_round)} | Total estimado: {_format_mmss(total_est)}", icon="⏲️")
    else:
        st.warning("No hay pasos definidos.", icon="⚠️")

    st.divider()

    # --------- Controles ----------
    c1, c2, c3, c4 = st.columns([1,1,1,2])

    with c1:
        if not st.session_state.hiit_running:
            st.button("▶️ Iniciar", use_container_width=True, on_click=_start_session, args=(steps, rounds))
        elif st.session_state.hiit_paused:
            st.button("⏯️ Reanudar", use_container_width=True, on_click=_resume_session)
        else:
            st.button("⏸️ Pausa", use_container_width=True, on_click=_pause_session)

    with c2:
        st.button("⏭️ Siguiente fase", use_container_width=True,
                  on_click=_advance_phase, args=(steps, int(rounds)))

    with c3:
        st.button("⏹️ Reset", use_container_width=True, on_click=_reset_session)

    with c4:
        st.toggle("Bloquear configuración al iniciar", value=st.session_state.hiit_config_locked,
                  key="hiit_config_locked", disabled=st.session_state.hiit_running)

    st.divider()

    # --------- Panel de estado + Progreso (render reactivo) ----------
    status = st.empty()
    pb = st.empty()

    # Auto-refresh para no bloquear la UI. 200 ms = 5 fps aprox.
    st.autorefresh(interval=200, key="hiit_tick")

    if st.session_state.hiit_running and st.session_state.hiit_phase_ends_at:
        now = time.time()
        remaining = st.session_state.hiit_phase_ends_at - now

        i = st.session_state.hiit_step_idx
        # Seguridad si se borraron filas en caliente
        if i >= len(steps):
            _reset_session()
            st.stop()

        phase = st.session_state.hiit_phase
        current_row = steps.iloc[i]
        total_phase = int(current_row["work_s"] if phase == "work" else current_row["rest_s"])
        if total_phase <= 0:
            # Evita divisiones por cero y fases vacías
            _advance_phase(steps, int(rounds))
            st.rerun()

        label = f"{current_row['name']} ({'Trabajo' if phase=='work' else 'Descanso'})"
        remaining_disp = _format_mmss(remaining)

        status.markdown(
            f"**Ronda:** {st.session_state.hiit_round}/{int(rounds)}  |  "
            f"**Paso:** {i+1}/{len(steps)}  |  "
            f"**Fase:** `{phase}`  |  **Tiempo:** {remaining_disp}  |  **{label}**"
        )

        elapsed = total_phase - max(0, remaining)
        pb.progress(min(1.0, max(0.0, elapsed / total_phase)))

        # Cambio de fase
        if remaining <= 0:
            _advance_phase(steps, int(rounds))
            st.rerun()
    else:
        status.info("Listo para iniciar. Configura pasos y pulsa ▶️.", icon="💡")
        pb.progress(0.0)

# ------------------------- Notas rápidas -------------------------
# - Esta página no usa bucles bloqueantes ni threads.
# - Usa st.autorefresh para refresco suave.
# - Si quieres sonidos, tendrás que servir un audio corto y disparar st.audio en el cambio de fase.
```
