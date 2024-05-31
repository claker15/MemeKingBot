package meme.bot.domain.superclasses;


import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;

import java.util.Date;

@MappedSuperclass
public class DatabaseObject {

    @Id
    private Long id;
    private Date created;
    private String guildId;
    private String userId;

}
