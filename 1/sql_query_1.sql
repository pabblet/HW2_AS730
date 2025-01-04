SELECT
    i.specObjID as ID,
    i.z as z,
    e.lgm_tot_p50 as stellarM,
    e.sfr_tot_p50 as SFR,
    e.oh_p50 as OH
FROM galSpecInfo AS i
JOIN galSpecExtra AS e ON i.specObjID = e.specObjID
WHERE i.z > 0.005 AND i.z < 0.3
    AND e.sfr_tot_p50 > -2 AND e.sfr_tot_p50 < 2
    AND e.lgm_tot_p50 != -9999
    AND e.sfr_tot_p50 != -9999
    AND e.oh_p50 != -9999
    AND e.bptclass = 1