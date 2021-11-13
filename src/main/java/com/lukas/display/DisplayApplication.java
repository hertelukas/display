package com.lukas.display;

import com.lukas.display.model.User;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DisplayApplication {

    private static User user;

    public static void main(String[] args) {
        SpringApplication.run(DisplayApplication.class, args);


        user = User.load();

        if(user == null){
            user = new User();        }

    }

    public static User getUser() {
        return user;
    }
}
