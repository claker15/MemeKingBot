package meme.bot.factory;

import net.dv8tion.jda.api.utils.messages.MessageCreateBuilder;
import net.dv8tion.jda.api.utils.messages.MessageCreateData;
import org.springframework.util.ResourceUtils;

import javax.imageio.ImageIO;
import java.io.File;
import java.io.InputStream;

public class ResponseMessageFactory {


    public static MessageCreateData buildResponseMessage(String type, String ...args) {

        MessageCreateBuilder builder = new MessageCreateBuilder();

        switch (type) {
            case "cringe":
                builder.addContent("<@%s> Cringe. Old meme, :b:ruh. Last posted at %s by <@%s> https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".formatted((Object[]) args));
                break;
            case "relax":
                builder.addContent("<@%s>. <@%s>, enjoy the point".formatted((Object[]) args));
                try {
                    InputStream stream = ResponseMessageFactory.class.getResourceAsStream("resources/images/Relax.png");
                    //TODO: figures this out
                    //                    builder.addFiles((MessageCreateFields.File.of("relax.png", stream));
                }
                catch (Exception e) {
                    System.out.println(e.getMessage());
                }
                break;
            case "equip":
                builder.addContent("You're lucky. Your spell had the added effect of %s points".formatted((Object[]) args));
                break;
            default:
                builder.addContent("Could not find correct message type");

        }

        return builder.build();

    }

}
