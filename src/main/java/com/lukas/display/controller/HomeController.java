package com.lukas.display.controller;

import com.lukas.display.DisplayApplication;
import com.lukas.display.model.User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class HomeController {

    @GetMapping("")
    public String home(Model model) {
        model.addAttribute("initialized", DisplayApplication.isInitialized());
        return "home";
    }

    @PostMapping("/setup")
    public String setup(){
        DisplayApplication.setUser(new User());
        return "redirect:/";
    }
}
