

function gitInfo(){
  [ -d .git ] || return

  BRANCH=$(git branch 2>/dev/null | grep -oP '(?<=^\*\s)(.*)')
  if [[ ! -z "$BRANCH" ]]; then
    ADDED=$(git status -s | awk 'BEGIN {c=0;} {if ($1 == "A") c+=1} END {print c}')
    MODIFIED=$(git status -s | awk 'BEGIN {c=0;} {if ($1 == "M") c+=1} END {print c}')
    DELETED=$(git status -s | awk 'BEGIN {c=0;} {if ($1 == "D") c+=1} END {print c}')
    UNTRACKED=$(git status -s | awk 'BEGIN {c=0;} {if ($1 == "??") c+=1} END {print c}')
    # printf "(\uE0A0%s|+%s~%s|-%s|?%s|)" $BRANCH $ADDED $MODIFIED $DELETED $UNTRACKED;
    printf "(\uE0A0%s +%s ~%s -%s ?%s)" $BRANCH $ADDED $MODIFIED $DELETED $UNTRACKED;
  fi;	
}

function gitColor(){
    GREEN="\e[1;32m"
    RED="\e[1;31m"
    [[ "$(git status --porcelain 2>/dev/null | wc -l)" -gt 0 ]] && printf $RED || printf $GREEN
}

function customPrompt(){
    local ec="$?"
    local RESET="\[\e[0m\]"
    local FG_RED="\[\e[1;31m\]"
    local FG_GREEN="\[\e[1;32m\]"
    local FG_YELLOW="\[\e[1;93m\]"
    local FG_BLUE="\[\e[1;34m\]"
    local FG_PURPLE="\[\e[1;35m\]"

    prompt=""┌""
    # prompt+="[$FG_YELLOW$(date -Is | cut -d + -f 1)$RESET]"
    prompt+="[${FG_YELLOW}\D{%Y-%m-%dT%H:%M:%S}${RESET}]"
    prompt+="[${FG_RED}\u${RESET}@${FG_BLUE}\h${RESET}]"
    prompt+="[${FG_GREEN}\w${RESET}]"
    prompt+="$(gitColor)$(gitInfo)${RESET}"
    prompt+="\n"
    prompt+="└"
    [[ $ec -eq  0 ]] && prompt+="$FG_GREEN" || prompt+="$FG_RED"
    prompt+=">$RESET "
    # printf $prompt
    PS1="$prompt"
    return $ec
}
PROMPT_COMMAND=('customPrompt')

