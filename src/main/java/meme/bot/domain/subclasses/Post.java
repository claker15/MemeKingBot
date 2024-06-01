package meme.bot.domain.subclasses;

import meme.bot.domain.superclasses.DatabaseObject;

public class Post extends DatabaseObject {

    private String hash;

    private String messageId;

    public Post(String userId, String guildId, String hash, String messageId) {
        super(userId, guildId);
        this.hash = hash;
        this.messageId = messageId;
    }

    public String getHash() {
        return hash;
    }

    public String getMessageId() {
        return messageId;
    }
}
