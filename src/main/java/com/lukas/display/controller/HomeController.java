package com.lukas.display.controller;

import com.lukas.display.DisplayApplication;
import com.lukas.display.form.GeneralForm;
import com.lukas.display.model.User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
public class HomeController {

    @GetMapping("")
    public String home(Model model) {
        User user = DisplayApplication.getUser();
        model.addAttribute("iCal", user.getiCalString());
        model.addAttribute("lat", user.getLat());
        model.addAttribute("lon", user.getLon());
        return "home";
    }

    @PostMapping("/general")
    public String handleGeneral(GeneralForm body) {
        System.out.println("General received: " + body);
        DisplayApplication.getUser().update(body);
        return "redirect:/";
    }

    @PostMapping("/display")
    public String handleDisplay(@RequestBody String body) {
        System.out.println("Display received: " + body);
        return "redirect:/";
    }

}
