package meme.bot.commands;

import meme.bot.service.BettingService;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import org.springframework.beans.factory.annotation.Autowired;

public class Bet implements SlashCommand{

    @Autowired
    private BettingService bettingService;

    @Override
    public void handle(SlashCommandInteractionEvent event) {

//        Mono<User> user = event.getOption("User")
//                .flatMap(ApplicationCommandInteractionOption::getValue)
//                .map(ApplicationCommandInteractionOptionValue::asUser)
//                .get();
//        Double points = event.getOption("Points")
//                .flatMap(ApplicationCommandInteractionOption::getValue)
//                .map(ApplicationCommandInteractionOptionValue::asDouble)
//                .get();
//        boolean result = bettingService.takeBet(user, points);
//        return null;
    }
}
