package meme.bot;

import meme.bot.service.MessageService;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.annotation.Bean;

import java.util.List;

@SpringBootApplication
@EnableAutoConfiguration
public class MemeKingBotApplication {

	@Value("${bot.token}")
	private String botToken;

	@Value("#{'${bot.channels.messages}'.split(',')}")
	private List<String> listeningChannels;

	@Autowired
	private MessageService messageService;

	public static void main(String[] args) {
		//Start spring application
		new SpringApplicationBuilder(MemeKingBotApplication.class)
				.build()
				.run(args);
	}


	@Bean
	public JDA botClient() {
		return JDABuilder.createDefault(botToken).build();
	}

}
