# hiit_tab.py
import time
import pandas as pd
import streamlit as st

def _init_state():
    for k, v in {
        "hiit_running": False,
        "hiit_paused": False,
        "hiit_round": 1,
        "hiit_step_idx": 0,
        "hiit_phase": "work",  # "work" | "rest"
        "hiit_phase_ends_at": None,
        "hiit_config_locked": False,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _advance_phase(steps, total_rounds):
    i = st.session_state.hiit_step_idx
    phase = st.session_state.hiit_phase

    # Datos del paso actual
    row = steps.iloc[i]
    work_s = int(row["work_s"])
    rest_s = int(row["rest_s"])

    if phase == "work":
        # Si había trabajo programado y acaba, pasamos a descanso si > 0, si no al siguiente paso
        if rest_s > 0:
            st.session_state.hiit_phase = "rest"
            st.session_state.hiit_phase_ends_at = time.time() + rest_s
        else:
            # No hay descanso, avanzamos de paso
            _advance_to_next_step(steps, total_rounds)
    else:
        # Terminó descanso, avanzamos de paso
        _advance_to_next_step(steps, total_rounds)

def _advance_to_next_step(steps, total_rounds):
    # Siguiente paso o siguiente ronda
    if st.session_state.hiit_step_idx + 1 < len(steps):
        st.session_state.hiit_step_idx += 1
        st.session_state.hiit_phase = "work"
        next_work = int(steps.iloc[st.session_state.hiit_step_idx]["work_s"])
        st.session_state.hiit_phase_ends_at = time.time() + next_work
    else:
        # Fin de la vuelta
        if st.session_state.hiit_round < total_rounds:
            st.session_state.hiit_round += 1
            st.session_state.hiit_step_idx = 0
            st.session_state.hiit_phase = "work"
            next_work = int(steps.iloc[0]["work_s"])
            st.session_state.hiit_phase_ends_at = time.time() + next_work
        else:
            # Fin total
            st.session_state.hiit_running = False
            st.session_state.hiit_paused = False
            st.session_state.hiit_config_locked = False

def _format_mmss(seconds):
    seconds = max(0, int(seconds))
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"

def render_hiit_tab():
    _init_state()

    tab, = st.tabs(["HIIT"])
    with tab:
        st.subheader("Timer HIIT configurable")

        # Config inicial por defecto
        default_df = pd.DataFrame([
            {"name": "Ejercicio 1", "work_s": 30, "rest_s": 30},
            {"name": "Ejercicio 2", "work_s": 30, "rest_s": 30},
            {"name": "Ejercicio 3", "work_s": 30, "rest_s": 30},
            {"name": "Ejercicio 4", "work_s": 30, "rest_s": 30},
        ])

        st.caption("Edita pasos, añade o borra filas. Tiempos en segundos.")
        disabled = st.session_state.hiit_config_locked

        steps = st.data_editor(
            default_df if "hiit_steps_df" not in st.session_state else st.session_state.hiit_steps_df,
            num_rows="dynamic",
            use_container_width=True,
            disabled=disabled,
            key="hiit_steps_df",
            column_config={
                "name": st.column_config.TextColumn("Paso"),
                "work_s": st.column_config.NumberColumn("Trabajo (s)", min_value=0, step=5),
                "rest_s": st.column_config.NumberColumn("Descanso (s)", min_value=0, step=5),
            }
        )

        colA, colB, colC = st.columns(3)
        with colA:
            rounds = st.number_input("Rondas", min_value=1, max_value=99, value=1, step=1, disabled=disabled, key="hiit_rounds_input")
        with colB:
            st.toggle("Pitido fin de fase (simple)", value=False, key="hiit_beep", disabled=True)  # placeholder
        with colC:
            st.toggle("Vibración móvil", value=False, key="hiit_vibrate", disabled=True)  # placeholder

        # Resumen rápido del total estimado
        if len(steps) > 0:
            per_round = int(steps["work_s"].fillna(0).sum() + steps["rest_s"].fillna(0).sum())
            total_est = per_round * int(rounds)
            st.caption(f"Tiempo por ronda aprox: {_format_mmss(per_round)} | Total aprox: {_format_mmss(total_est)}")

        # Controles
        c1, c2, c3 = st.columns(3)
        def start():
            if len(steps) == 0:
                return
            st.session_state.hiit_running = True
            st.session_state.hiit_paused = False
            st.session_state.hiit_config_locked = True
            # Reset de índices si veníamos de stop
            if st.session_state.hiit_phase_ends_at is None or st.session_state.hiit_round > st.session_state.hiit_rounds_input:
                st.session_state.hiit_round = 1
                st.session_state.hiit_step_idx = 0
                st.session_state.hiit_phase = "work"
            # Arrancamos el temporizador de la fase actual
            current_work = int(steps.iloc[st.session_state.hiit_step_idx]["work_s"])
            st.session_state.hiit_phase_ends_at = time.time() + current_work

        def pause():
            st.session_state.hiit_paused = True

        def resume():
            # Recalcular fin sumando el tiempo restante actual
            remaining = st.session_state.hiit_phase_ends_at - time.time()
            st.session_state.hiit_phase_ends_at = time.time() + max(0, remaining)
            st.session_state.hiit_paused = False

        def reset():
            st.session_state.hiit_running = False
            st.session_state.hiit_paused = False
            st.session_state.hiit_round = 1
            st.session_state.hiit_step_idx = 0
            st.session_state.hiit_phase = "work"
            st.session_state.hiit_phase_ends_at = None
            st.session_state.hiit_config_locked = False

        with c1:
            if not st.session_state.hiit_running:
                st.button("▶️ Iniciar", on_click=start, use_container_width=True)
            elif st.session_state.hiit_paused:
                st.button("⏯️ Reanudar", on_click=resume, use_container_width=True)
            else:
                st.button("⏸️ Pausa", on_click=pause, use_container_width=True)

        with c2:
            st.button("⏹️ Reset", on_click=reset, use_container_width=True)
        with c3:
            st.button("🔁 Siguiente fase", use_container_width=True,
                      on_click=lambda: _advance_phase(steps, int(rounds)))

        # Panel de estado
        st.divider()
        status = st.empty()
        pb = st.empty()

        if st.session_state.hiit_running and st.session_state.hiit_phase_ends_at:
            # Bucle de render controlado
            while st.session_state.hiit_running and not st.session_state.hiit_paused:
                now = time.time()
                remaining = st.session_state.hiit_phase_ends_at - now

                # Info actual
                i = st.session_state.hiit_step_idx
                phase = st.session_state.hiit_phase
                current_row = steps.iloc[i]
                label = f"{current_row['name']} ({'Trabajo' if phase=='work' else 'Descanso'})"
                total_phase = int(current_row["work_s"] if phase == "work" else current_row["rest_s"]) or 1
                remaining_disp = _format_mmss(remaining)

                status.markdown(
                    f"**Ronda:** {st.session_state.hiit_round}/{int(rounds)}  |  "
                    f"**Paso:** {i+1}/{len(steps)}  |  "
                    f"**Fase:** `{phase}`  |  **Tiempo:** {remaining_disp}  |  **{label}**"
                )

                # Progress
                elapsed = total_phase - max(0, remaining)
                pb.progress(min(1.0, max(0.0, elapsed / total_phase)))

                if remaining <= 0:
                    _advance_phase(steps, int(rounds))
                    # Tras avanzar, salimos para que Streamlit re-renderice limpio
                    st.experimental_rerun()

                time.sleep(0.1)

        # Tip rápido
        st.caption("Tip: bloquea la configuración al iniciar. Edita pasos y tiempos libremente antes de darle a Iniciar.")

# Si lo quieres en una página existente:
# import streamlit as st
# from hiit_tab import render_hiit_tab
# render_hiit_tab()
