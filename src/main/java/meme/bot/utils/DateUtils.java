package meme.bot.utils;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class DateUtils {


    public static List<Date> getCurrentWeekBeginningAndEndDates() {
        List<Date> dates = new ArrayList<>();
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.HOUR, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);

        cal.set(Calendar.DAY_OF_WEEK, cal.getFirstDayOfWeek());
        dates.add(cal.getTime());

        cal.add(Calendar.WEEK_OF_YEAR, 1);
        dates.add(cal.getTime());

        return dates;
    }

    public static List<Date> getLastWeekBeginningAndEndDates() {
        List<Date> dates = new ArrayList<>();
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.HOUR, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);

        cal.set(Calendar.DAY_OF_WEEK, cal.getFirstDayOfWeek());
        cal.add(Calendar.WEEK_OF_YEAR, -1);
        dates.add(cal.getTime());

        cal.add(Calendar.WEEK_OF_YEAR, 1);
        dates.add(cal.getTime());

        return dates;
    }


}
