//package meme.bot.domain;
//
//import discord4j.core.object.entity.User;
//import reactor.core.publisher.Mono;
//
//public class BetRequest {
//
//
//    private Mono<User> userMono;
//
//    private Mono<Integer> pointsMono;
//
//    public BetRequest(Mono<User> userMono, Mono<Integer> pointsMono) {
//        this.userMono = userMono;
//        this.pointsMono = pointsMono;
//    }
//
//    public Mono<User> getUserMono() {
//        return userMono;
//    }
//
//    public void setUserMono(Mono<User> userMono) {
//        this.userMono = userMono;
//    }
//
//    public Mono<Integer> getPointsMono() {
//        return pointsMono;
//    }
//
//    public void setPointsMono(Mono<Integer> pointsMono) {
//        this.pointsMono = pointsMono;
//    }
//}
