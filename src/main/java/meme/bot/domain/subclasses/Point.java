package meme.bot.domain.subclasses;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import meme.bot.domain.superclasses.DatabaseObject;

@Entity
@Table(name = "points")
public class Point extends DatabaseObject {

    private Integer pointValue;
    private String type;

    private String userIdFrom;

    private String messageId;

    public Point() {
        super();
    }

    public Point(String userId, String guildId, Integer value, String type, String userIdFrom, String messageId) {
        super(userId, guildId);
        this.pointValue = value;
        this.type = type;
        this.userIdFrom = userIdFrom;
        this.messageId = messageId;
    }

}
