package meme.bot.domain.subclasses;

import jakarta.persistence.Entity;
import meme.bot.domain.superclasses.DatabaseObject;

@Entity
public class Point extends DatabaseObject {

    private Integer value;
    private String type;

    private String userIdFrom;

    private String messageId;

}
