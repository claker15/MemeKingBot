package meme.bot.utils;

import discord4j.core.event.domain.Event;
import discord4j.core.event.domain.message.MessageCreateEvent;
import discord4j.core.object.entity.Message;

public class MessageInfo {

    private String authorId;
    private String guildId;
    private String messageId;

    private String channelId;

    private MessageCreateEvent event;

    private Message message;

    public MessageInfo(MessageCreateEvent event) {
        this.event = event;
        this.message = event.getMessage();
        this.authorId = message.getAuthor().get().getId().asString();
        this.guildId = message.getGuildId().get().asString();
        this.messageId = message.getId().asString();
        this.channelId = message.getChannelId().asString();

    }

    public String getAuthorId() {
        return authorId;
    }

    public String getGuildId() {
        return guildId;
    }

    public String getMessageId() {
        return messageId;
    }

    public String getChannelId() {
        return channelId;
    }

    public MessageCreateEvent getEvent() {
        return event;
    }

    public Message getMessage() {
        return message;
    }
}
