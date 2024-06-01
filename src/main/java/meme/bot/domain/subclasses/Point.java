package meme.bot.domain.subclasses;

import jakarta.persistence.Entity;
import meme.bot.domain.superclasses.DatabaseObject;

@Entity
public class Point extends DatabaseObject {

    private Integer value;
    private String type;

    private String userIdFrom;

    private String messageId;

    public Point(String userId, String guildId, Integer value, String type, String userIdFrom, String messageId) {
        super(userId, guildId);
        this.value = value;
        this.type = type;
        this.userIdFrom = userIdFrom;
        this.messageId = messageId;
    }
}
