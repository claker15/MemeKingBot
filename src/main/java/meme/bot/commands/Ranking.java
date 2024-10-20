package meme.bot.commands;

import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Ranking implements SlashCommand {

/*    @Autowired
    private RankingEmbedFactory rankingEmbedFactory;*/

    @Override
    public void handle(SlashCommandInteractionEvent event) {

        if (!event.getName().equals("ranking")) {
            return;
        }

    }
}
