package meme.bot.factory;

import discord4j.core.spec.MessageCreateFields;
import discord4j.core.spec.MessageCreateSpec;

import javax.imageio.ImageIO;

public class ResponseMessageFactory {


    public static MessageCreateSpec buildResponseMessage(String type, String ...args) {

        MessageCreateSpec.Builder messageSpec = MessageCreateSpec.builder();

        switch (type) {
            case "cringe":
                messageSpec.content("%s Cringe. Old meme, :b:ruh. Last posted at %s by %s https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".formatted((Object[]) args));
                break;
            case "relax":
                messageSpec.content("{0}. {1}, enjoy the point".formatted((Object[]) args));
                try {
                    messageSpec.addFile((MessageCreateFields.File) ImageIO.read(ResponseMessageFactory.class.getClassLoader().getResource("/resources/images/Relax.png")));
                }
                catch (Exception e) {

                }
                break;
            case "equip":
                messageSpec.content("You're lucky. Your spell had the added effect of %s points".formatted((Object[]) args));
                break;
            default:
                messageSpec.content("Could not find correct message type");

        }

        return messageSpec.build();

    }

}
