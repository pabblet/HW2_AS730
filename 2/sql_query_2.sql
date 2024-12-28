SELECT TOP 100
    i.specObjID as ID,
    i.z as z,
    l.h_alpha_flux as Halpha,
    l.h_beta_flux as Hbeta,
    l.h_alpha_flux/l.h_beta_flux as BalmerD,
    e.sfr_tot_p50 as SFR,
    dbo.fCosmoDl(i.z, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT)*3.086e24 as LD
FROM galSpecInfo AS i
JOIN galSpecLine AS l ON i.specObjID = l.specObjID
JOIN galSpecExtra AS e ON i.specObjID = e.specObjID
WHERE i.z > 0.005 
    AND l.h_alpha_flux > 5
    AND l.h_beta_flux > 5
    AND l.h_alpha_flux/l.h_beta_flux > 2.86