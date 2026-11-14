"""        ---
        ### 👥 Team AetherNova
        * **Annzita Joshi** – Team Lead, Development, Data Analysis & UI/UX
        * **Ashna Maria Saji** – NASA Dataset Research, Literature & Documentation Support
        
        ---
        ### 📑 June 2024 Scientific Validation Audit Summary
        * **NASA GPM IMERG Calculated (Kerala Terrestrial):** `404.00 mm`
        * **IMD Official Reference (Kerala & Mahe Subdivision):** `489.30 mm`
        * **Discrepancy:** `-85.30 mm (-17.43%)`
        * **Methodological Distinction:** NASA GPM IMERG is a spaceborne microwave-infrared gridded reanalysis product over a Kerala-only polygon. IMD utilizes surface rain gauge interpolation across the Kerala & Mahe meteorological subdivision. Satellite sensors experience orographic warm-rain undercatch over the steep Western Ghats. NASA data is independent and is not calibrated to IMD regional networks.
        """
# -----------------------------------------------------------------------------
# 5. Application Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-text">
        <strong>AetherNova</strong> – <em>Decoding Rainfall. Discovering Patterns.</em> | NASA Space Apps Challenge 2026<br>
        Kerala Rainfall Trend Detective • Developed by Annzita Joshi & Ashna Maria Saji
    </div>
    """),
    unsafe_allow_html=True,
)
