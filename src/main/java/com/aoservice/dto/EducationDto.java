package com.aoservice.dto;

import java.util.Date;

public class EducationDto {
    private Long id;
    private String nomEcole;
    private String typeDiplome;
    private Date dateDebut;
    private Date dateFin;

    public EducationDto() {
    }

    public EducationDto(Long id,String nomEcole, String typeDiplome, Date dateDebut, Date dateFin) {
        this.id=id;
        this.nomEcole = nomEcole;
        this.typeDiplome = typeDiplome;
        this.dateDebut = dateDebut;
        this.dateFin = dateFin;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNomEcole() {
        return nomEcole;
    }

    public void setNomEcole(String nomEcole) {
        this.nomEcole = nomEcole;
    }

    public String getTypeDiplome() {
        return typeDiplome;
    }

    public void setTypeDiplome(String typeDiplome) {
        this.typeDiplome = typeDiplome;
    }

    public Date getDateDebut() {
        return dateDebut;
    }

    public void setDateDebut(Date dateDebut) {
        this.dateDebut = dateDebut;
    }

    public Date getDateFin() {
        return dateFin;
    }

    public void setDateFin(Date dateFin) {
        this.dateFin = dateFin;
    }
}
