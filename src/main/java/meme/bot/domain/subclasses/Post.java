package meme.bot.domain.subclasses;

import jakarta.persistence.Entity;
import meme.bot.domain.superclasses.DatabaseObject;

import java.math.BigInteger;

@Entity
public class Post extends DatabaseObject {

    private BigInteger hash;

    private String messageId;

    public Post() {
    }

    public Post(String userId, String guildId, BigInteger hash, String messageId) {
        super(userId, guildId);
        this.hash = hash;
        this.messageId = messageId;
    }

    public BigInteger getHash() {
        return hash;
    }

    public String getMessageId() {
        return messageId;
    }
}
