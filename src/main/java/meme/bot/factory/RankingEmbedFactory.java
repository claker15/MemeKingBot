package meme.bot.factory;

import discord4j.common.util.Snowflake;
import discord4j.core.DiscordClient;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.spec.EmbedCreateSpec;
import discord4j.core.spec.MessageCreateFields;
import discord4j.core.spec.MessageCreateSpec;
import discord4j.rest.util.Color;
import meme.bot.domain.subclasses.User;
import meme.bot.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.imageio.ImageIO;
import java.util.ArrayList;
import java.util.List;

@Component
public class RankingEmbedFactory {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    GatewayDiscordClient gatewayDiscordClient;

    public EmbedCreateSpec buildRankingMessage(String type, String ...args) {

        EmbedCreateSpec.Builder embedSpec = EmbedCreateSpec.builder();

        List<User> users = new ArrayList<>();
        switch (type) {
            case "ranking":
                users = userRepository.getWeeklyUserRankings(args[0]);
                embedSpec.title("Current Meme King Rankings");
                embedSpec.color(Color.BLUE);
                break;

            default:


        }
        users.forEach(user -> {
            String userNick = String.valueOf(gatewayDiscordClient.getUserById(Snowflake.of(user.getUserId())).map(discord4j.core.object.entity.User::getUsername));
            embedSpec.addField(userNick, user.getUserId(), false);
        });
        return embedSpec.build();

    }


}
