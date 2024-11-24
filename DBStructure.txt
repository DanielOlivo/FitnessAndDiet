APIManager.py
	empty
app.py
	empty
body_fat_index.py this is out
	calculate_body_fat()
clean.py
	reset the database
db_test.py
	clean(date)
	test_all(self)
engine.py
	url_object ()
graphs.py
	graph_rep()
location.py
	get_geolocation()
	find_nearby_studios
main_front.py
	main()
menu_messages.py
	welcome_message
	handle_new_user()
	handle_log_in()
	handle_centers()
	handle_new_alarms(schedule)
	handle_schedules(user)
	get_past_and_incoming_alarms(alarms)
	handle_commands(user)
	main()
models.py
	class Base
	class User(Base)
	class FitnessCenter(Base)
	class FitnessSubscription(Base)
	class Schedule(Base)
	class Alarm (Base)
	class Attendance (Base)
	class Profile(Base)
reminder.py
	create_event(summary, start_time, end_time)
	notify_user()
utils.py
	create_database()
	drop_database()
	reset_database()
	create_user()
	user_exists()
	get_user_by_last_name(last_name)
	get_first_user()
	get_users()
	get_user_by_fullname(firstname, lastname)
	get_users_after(datetime)
	delete_user(user)
	delete_users_after(date)
	create_center(name, address)
	center_exists(name)
	delete_center(center)
	delete_centers_after(date)
	get_centers()
	get_centers_after(date)
	get_center_by_name(name)
	get_user_centers(user)
	add_subscription(user, center)
	get_user_subscriptions(user)
	delete_subscription(subscription)
	delete_subscriptions_after(date)
	get_subscriptions()
	get_subscriptions_after(date)
	add_schedule(user, center)
	remove_schedule(schedule)
	get_schedules(user)
	get_alarms(schedule)
	get_alarms_after(date)
	add_alarm(schedule, day_of_week, hours, minutes, duration)
	update_alarm(alarm, day_of_week=None, hours=None, minutes=None, duration=None)
	delete_alarm(alarm)
	delete_alarms_after(date)
	add_profile(user, height, weight, notification)
	get_last_profile(user)
	delete_profile(profile)
	get_profiles(user)
	get_profiles_after(date)
	delete_profiles_after(date)
	add_attendence(alarm, time, attendent)
	show_stmts()
weekly_stats.py
	get_weekly_stats(user_id)
	fetch_quote()
	