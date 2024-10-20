package meme.bot.commands;

public class CommandFactory {


    public static SlashCommand createCommand(String commandName) {

        return switch (commandName) {
            case "bet" -> new Bet();
            case "ranking" -> new Ranking();
            default -> new Ping();
        };

    }

}
