package com.aoservice.dto;

import javax.persistence.Column;
import java.sql.Timestamp;

public class ContratDto {
    private Long id;
    private String idCandidature;
    private String refAo;
    private String nomSocieteClient;
    private String formeJuriqiqueClient;
    private String capitaleSocieteClient;
    private String lieuSiegeClient;
    private String numeroRegitreCommerceClient;
    private String nomRepresentantSocieteClient;
    private String nomPrestataire;
    private String prenomPrestataire;
    private String lieuPrestataire;
    private String cin;
    private String preambule;
    private Float prixTotaleMission;
    private Float penalisationParJour;
    @Column(nullable = false, updatable = false)
    private Timestamp dateGenerationContrat;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getIdCandidature() {
        return idCandidature;
    }

    public void setIdCandidature(String idCandidature) {
        this.idCandidature = idCandidature;
    }

    public String getNomSocieteClient() {
        return nomSocieteClient;
    }

    public void setNomSocieteClient(String nomSocieteClient) {
        this.nomSocieteClient = nomSocieteClient;
    }

    public String getFormeJuriqiqueClient() {
        return formeJuriqiqueClient;
    }

    public void setFormeJuriqiqueClient(String formeJuriqiqueClient) {
        this.formeJuriqiqueClient = formeJuriqiqueClient;
    }



    public String getLieuSiegeClient() {
        return lieuSiegeClient;
    }

    public void setLieuSiegeClient(String lieuSiegeClient) {
        this.lieuSiegeClient = lieuSiegeClient;
    }


    public String getNomRepresentantSocieteClient() {
        return nomRepresentantSocieteClient;
    }

    public void setNomRepresentantSocieteClient(String nomRepresentantSocieteClient) {
        this.nomRepresentantSocieteClient = nomRepresentantSocieteClient;
    }

    public String getNomPrestataire() {
        return nomPrestataire;
    }

    public void setNomPrestataire(String nomPrestataire) {
        this.nomPrestataire = nomPrestataire;
    }

    public String getPrenomPrestataire() {
        return prenomPrestataire;
    }

    public void setPrenomPrestataire(String prenomPrestataire) {
        this.prenomPrestataire = prenomPrestataire;
    }

    public String getLieuPrestataire() {
        return lieuPrestataire;
    }

    public void setLieuPrestataire(String lieuPrestataire) {
        this.lieuPrestataire = lieuPrestataire;
    }

    public String getPreambule() {
        return preambule;
    }

    public void setPreambule(String preambule) {
        this.preambule = preambule;
    }

    public Float getPrixTotaleMission() {
        return prixTotaleMission;
    }

    public void setPrixTotaleMission(Float prixTotaleMission) {
        this.prixTotaleMission = prixTotaleMission;
    }

    public Float getPenalisationParJour() {
        return penalisationParJour;
    }

    public void setPenalisationParJour(Float penalisationParJour) {
        this.penalisationParJour = penalisationParJour;
    }

    public Timestamp getDateGenerationContrat() {
        return dateGenerationContrat;
    }

    public void setDateGenerationContrat(Timestamp dateGenerationContrat) {
        this.dateGenerationContrat = dateGenerationContrat;
    }

    public String getRefAo() {
        return refAo;
    }

    public void setRefAo(String refAo) {
        this.refAo = refAo;
    }

    public String getCapitaleSocieteClient() {
        return capitaleSocieteClient;
    }

    public void setCapitaleSocieteClient(String capitaleSocieteClient) {
        this.capitaleSocieteClient = capitaleSocieteClient;
    }

    public String getNumeroRegitreCommerceClient() {
        return numeroRegitreCommerceClient;
    }

    public void setNumeroRegitreCommerceClient(String numeroRegitreCommerceClient) {
        this.numeroRegitreCommerceClient = numeroRegitreCommerceClient;
    }

    public String getCin() {
        return cin;
    }

    public void setCin(String cin) {
        this.cin = cin;
    }
}
