package meme.bot.listener;

import meme.bot.commands.CommandFactory;
import meme.bot.commands.SlashCommand;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;


@Component
public class SlashCommandListener extends ListenerAdapter {


    @Autowired
    private Map<String, SlashCommand> commandMap;

    @Override
    public void onSlashCommandInteraction(SlashCommandInteractionEvent event) {

        SlashCommand command = CommandFactory.createCommand(event.getName());
        command.handle(event);

    }
}
