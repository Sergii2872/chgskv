// скрипт для celery progress bar https://github.com/czue/celery-progress
// подключаем в result_poloniex_kurscurrency.html, result_poloniex_namecurrency.html
$(function () {
  var progressUrl = "{% url 'progress_view:task_status' task_id %}";
  CeleryProgressBar.initProgressBar(progressUrl)
});