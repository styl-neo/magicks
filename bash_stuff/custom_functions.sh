# Functions

sendNotification(){
  [[ -z "$1" ]] && return
  curl -sd "$1" 'ntfy.sh/stylneo-general' > /dev/null
}