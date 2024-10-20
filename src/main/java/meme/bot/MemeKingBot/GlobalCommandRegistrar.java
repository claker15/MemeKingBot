package meme.bot.MemeKingBot;


import com.fasterxml.jackson.databind.ObjectMapper;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Stream;

@Component
public class GlobalCommandRegistrar implements ApplicationRunner {
    private final Logger LOGGER = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private JDA jda;

    //Use the rest client provided by our Bean
    public GlobalCommandRegistrar(JDA jda) {
        this.jda = jda;
    }

    //This method will run only once on each start up and is automatically called with Spring so blocking is okay.
    @Override
    public void run(ApplicationArguments args) throws IOException, URISyntaxException {

        CommandListUpdateAction commands = jda.updateCommands();

        commands.addCommands(
                Commands.slash("bet", "Place a bet")
                        .addOption(OptionType.STRING, "user", "User who you wish to bet on", true)
                        .addOption(OptionType.INTEGER, "points", "Amount of points to bet", true),
                Commands.slash("ranking", "Get current week's rankings")
        );

        commands.queue();

    }

}