package com.lukas.display.form;

public class GeneralForm {
    private String iCal;
    private float lat;
    private float lon;

    public GeneralForm(String iCal, float lat, float lon) {
        this.iCal = iCal;
        this.lat = lat;
        this.lon = lon;
    }

    public float getLon() {
        return lon;
    }

    public float getLat() {
        return lat;
    }

    public String getiCal() {
        return iCal;
    }

    @Override
    public String toString() {
        return "GeneralForm{" +
                "iCal='" + iCal + '\'' +
                ", lat=" + lat +
                ", lon=" + lon +
                '}';
    }
}
