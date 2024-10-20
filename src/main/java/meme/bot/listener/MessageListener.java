package meme.bot.listener;

import meme.bot.service.MessageService;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.springframework.beans.factory.annotation.Autowired;

public class MessageListener extends ListenerAdapter {

    @Autowired
    private MessageService messageService;

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {

        if (event.getAuthor().isBot()) {
            return;
        }

        messageService.processMessage(event.getMessage());

    }

}
