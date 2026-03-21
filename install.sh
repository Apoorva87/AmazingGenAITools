#!/usr/bin/env bash
#
# install.sh — Install AmazingGenAITools skills and agents into Claude Code or Codex
#
# Skills are symlinked into .claude/skills/ or .codex/skills/
# Agents are symlinked into .claude/agents/ or .codex/agents/ depending on tool
#
# Usage:
#   ./install.sh              Interactive menu
#   ./install.sh --all        Install everything
#   ./install.sh --skills     Install all skills only
#   ./install.sh --agents     Install all agents only
#   ./install.sh --list       List available components
#   ./install.sh <name> ...   Install specific items by name

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"
AGENTS_SRC="$SCRIPT_DIR/agents"
TOOL=""
INSTALL_TARGET_SET=0
INSTALL_TARGET_NAME="repo"
TOOL_SET=0
DEEP_SCAN=0
MISSING_SKILL_NAMES=()
MISSING_SKILL_PATHS=()
MISSING_SKILL_LOCATIONS=()
MISSING_AGENT_NAMES=()
MISSING_AGENT_PATHS=()
MISSING_AGENT_LOCATIONS=()

configure_tool() {
  case "$1" in
    claude)
      TOOL="claude"
      TOOL_LABEL="Claude Code"
      REPO_TOOL_DIR="$SCRIPT_DIR/.claude"
      HOME_TOOL_DIR="$HOME/.claude"
      SUPPORTS_AGENTS=1
      AGENT_EXT="md"
      ;;
    codex)
      TOOL="codex"
      TOOL_LABEL="Codex"
      REPO_TOOL_DIR="$SCRIPT_DIR/.codex"
      HOME_TOOL_DIR="$HOME/.codex"
      SUPPORTS_AGENTS=1
      AGENT_EXT="toml"
      ;;
    *)
      echo "Unsupported tool: $1 (expected: claude or codex)"
      exit 1
      ;;
  esac

  TOOL_DIR="$REPO_TOOL_DIR"
  SKILLS_DST="$TOOL_DIR/skills"
  AGENTS_DST="$TOOL_DIR/agents"
  TOOL_SET=1
}

select_tool() {
  if [ "$TOOL_SET" -eq 1 ]; then
    return
  fi

  if [ ! -t 0 ]; then
    configure_tool "claude"
    return
  fi

  while true; do
    echo ""
    echo -e "${BOLD}Choose target tool:${RESET}"
    echo "  1) Claude Code"
    echo "  2) Codex"
    read -rp "Choice [1/2, default 1]: " choice
    case "$choice" in
      ""|1|claude)
        configure_tool "claude"
        break
        ;;
      2|codex)
        configure_tool "codex"
        break
        ;;
      *)
        echo -e "${YELLOW}Please enter 1 for Claude Code or 2 for Codex.${RESET}"
        ;;
    esac
  done
}

select_install_target() {
  select_tool

  if [ "${AI_INSTALL_TARGET:-}" = "home" ]; then
    TOOL_DIR="$HOME_TOOL_DIR"
    INSTALL_TARGET_NAME="home"
  elif [ "${AI_INSTALL_TARGET:-}" = "current" ] || [ "${AI_INSTALL_TARGET:-}" = "repo" ]; then
    TOOL_DIR="$REPO_TOOL_DIR"
    INSTALL_TARGET_NAME="repo"
  else
    if [ ! -t 0 ]; then
      TOOL_DIR="$REPO_TOOL_DIR"
      INSTALL_TARGET_NAME="repo"
    else
      while true; do
        echo ""
        echo -e "${BOLD}Choose ${TOOL_LABEL} install location:${RESET}"
        echo "  1) Current repo ($REPO_TOOL_DIR)"
        echo "  2) Home directory ($HOME_TOOL_DIR)"
        read -rp "Choice [1/2, default 1]: " choice
        case "$choice" in
          ""|1|current|repo)
            TOOL_DIR="$REPO_TOOL_DIR"
            INSTALL_TARGET_NAME="repo"
            break
            ;;
          2|home)
            TOOL_DIR="$HOME_TOOL_DIR"
            INSTALL_TARGET_NAME="home"
            break
            ;;
          *)
            echo -e "${YELLOW}Please enter 1 for repo or 2 for home.${RESET}"
            ;;
        esac
      done
    fi
  fi

  SKILLS_DST="$TOOL_DIR/skills"
  AGENTS_DST="$TOOL_DIR/agents"
  INSTALL_TARGET_SET=1
  echo -e "\nInstalling for ${BOLD}$TOOL_LABEL${RESET} into ${BOLD}$INSTALL_TARGET_NAME${RESET} directory ${DIM}($TOOL_DIR)${RESET}\n"
}

ensure_install_target() {
  if [ "$INSTALL_TARGET_SET" -eq 1 ]; then
    return
  fi
  select_install_target
}

# Colors (disabled if not a terminal)
if [ -t 1 ]; then
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  CYAN='\033[0;36m'
  RED='\033[0;31m'
  BOLD='\033[1m'
  DIM='\033[2m'
  RESET='\033[0m'
else
  GREEN='' YELLOW='' CYAN='' RED='' BOLD='' DIM='' RESET=''
fi

# ── Discovery ──────────────────────────────────────────────────────────────────

discover_skills() {
  local skills=()
  if [ -d "$SKILLS_SRC" ]; then
    for dir in "$SKILLS_SRC"/*/; do
      [ -f "$dir/SKILL.md" ] && skills+=("$(basename "$dir")")
    done
  fi
  echo "${skills[@]:-}"
}

discover_agents() {
  local agents=()
  if [ -d "$AGENTS_SRC" ]; then
    for file in "$AGENTS_SRC"/*."$AGENT_EXT"; do
      [ -f "$file" ] || continue
      local name
      name="$(basename "$file" ."$AGENT_EXT")"
      [ "$name" = "README" ] && continue
      agents+=("$name")
    done
  fi
  echo "${agents[@]:-}"
}

# ── Install helpers ────────────────────────────────────────────────────────────

install_skill() {
  local name="$1"
  local src="$SKILLS_SRC/$name"
  local dst="$SKILLS_DST/$name"

  if [ ! -d "$src" ] || [ ! -f "$src/SKILL.md" ]; then
    echo -e "  ${RED}x${RESET} Skill ${BOLD}$name${RESET} not found"
    return 1
  fi

  ensure_install_target
  mkdir -p "$SKILLS_DST"

  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    report_existing_install "Skill ${BOLD}$name${RESET}" "$src" "$dst"
    return 0
  fi

  if [ -e "$dst" ] || [ -L "$dst" ]; then
    report_existing_install "Skill ${BOLD}$name${RESET}" "$src" "$dst"
    rm -rf "$dst"
  fi

  ln -sf "$src" "$dst"
  echo -e "  ${GREEN}+${RESET} Skill ${BOLD}$name${RESET} installed"
}

print_diff_summary() {
  local src="$1"
  local dst="$2"
  if [ ! -e "$dst" ] && [ ! -L "$dst" ]; then
    return
  fi

  if diff -qr "$src" "$dst" >/dev/null 2>&1; then
    echo -e "    ${DIM}Matches the source directory${RESET}"
  else
    echo -e "    ${YELLOW}Differences from source:${RESET}"
    diff -ru "$src" "$dst" | sed 's/^/      /' || true
  fi
}

report_existing_install() {
  local label="$1"
  local src="$2"
  local dst="$3"
  echo -e "  ${DIM}-${RESET} ${label} already installed at ${BOLD}$TOOL_DIR${RESET}"
  print_diff_summary "$src" "$dst"
}

install_agent() {
  local name="$1"

  if [ "$SUPPORTS_AGENTS" -ne 1 ]; then
    echo -e "  ${YELLOW}!${RESET} Agents are not installed for ${BOLD}$TOOL_LABEL${RESET}; skipping ${BOLD}$name${RESET}"
    return 0
  fi

  local src="$AGENTS_SRC/${name}.${AGENT_EXT}"
  local dst="$AGENTS_DST/${name}.${AGENT_EXT}"

  if [ ! -f "$src" ]; then
    echo -e "  ${RED}x${RESET} Agent ${BOLD}$name${RESET} not found"
    return 1
  fi

  ensure_install_target
  mkdir -p "$AGENTS_DST"

  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    report_existing_install "Agent ${BOLD}$name${RESET}" "$src" "$dst"
    return 0
  fi

  if [ -f "$dst" ] && cmp -s "$src" "$dst"; then
    report_existing_install "Agent ${BOLD}$name${RESET}" "$src" "$dst"
    return 0
  fi

  if [ -e "$dst" ] || [ -L "$dst" ]; then
    report_existing_install "Agent ${BOLD}$name${RESET}" "$src" "$dst"
    rm -f "$dst"
  fi

  ln -sf "$src" "$dst"
  echo -e "  ${GREEN}+${RESET} Agent ${BOLD}$name${RESET} installed"
}

# ── List ───────────────────────────────────────────────────────────────────────

list_components() {
  local skills agents
  read -ra skills <<< "$(discover_skills)"
  read -ra agents <<< "$(discover_agents)"

  ensure_install_target

  echo -e "\n${BOLD}Available components for ${TOOL_LABEL}:${RESET}\n"

  echo -e "${CYAN}Skills${RESET} (${#skills[@]}):"
  for s in "${skills[@]}"; do
    local status="${DIM}not installed${RESET}"
    local dst="$SKILLS_DST/$s"
    [ -L "$dst" ] && status="${GREEN}installed${RESET}"
    echo -e "  $s  ($status)"
  done

  if [ "$SUPPORTS_AGENTS" -eq 1 ]; then
    echo ""
    echo -e "${CYAN}Agents${RESET} (${#agents[@]}):"
    for a in "${agents[@]}"; do
      local status="${DIM}not installed${RESET}"
      local dst="$AGENTS_DST/${a}.${AGENT_EXT}"
      [ -e "$dst" ] && status="${GREEN}installed${RESET}"
      echo -e "  $a  ($status)"
    done
  fi
  echo ""
}

copy_skill_into_repo() {
  local src_dir="$1"
  local skill_name="$2"

  mkdir -p "$SKILLS_SRC"
  if [ -e "$SKILLS_SRC/$skill_name" ]; then
    echo -e "  ${DIM}-${RESET} ${skill_name} already exists in source"
    return
  fi

  echo -e "  ${GREEN}+${RESET} Copying ${BOLD}$skill_name${RESET} into source"
  cp -R "$src_dir" "$SKILLS_SRC/$skill_name"
}

copy_agent_into_repo() {
  local src_file="$1"
  local agent_name="$2"
  local ext="${src_file##*.}"

  mkdir -p "$AGENTS_SRC"
  if [ -e "$AGENTS_SRC/${agent_name}.${ext}" ]; then
    echo -e "  ${DIM}-${RESET} ${agent_name} already exists in source"
    return
  fi

  echo -e "  ${GREEN}+${RESET} Copying ${BOLD}$agent_name${RESET} into source"
  cp "$src_file" "$AGENTS_SRC/${agent_name}.${ext}"
}

list_contains() {
  local needle="$1"
  shift
  for item in "$@"; do
    [ "$item" = "$needle" ] && return 0
  done
  return 1
}

register_missing_skill() {
  local name="$1"
  local path="$2"
  local location="$3"

  if [ -d "$SKILLS_SRC/$name" ]; then
    return
  fi

  if [ ${#MISSING_SKILL_NAMES[@]} -gt 0 ] && list_contains "$name" "${MISSING_SKILL_NAMES[@]}"; then
    return
  fi

  MISSING_SKILL_NAMES+=("$name")
  MISSING_SKILL_PATHS+=("$path")
  MISSING_SKILL_LOCATIONS+=("$location")
}

register_missing_agent() {
  local name="$1"
  local path="$2"
  local location="$3"

  if [ -f "$AGENTS_SRC/${name}.md" ] || [ -f "$AGENTS_SRC/${name}.toml" ]; then
    return
  fi

  if [ ${#MISSING_AGENT_NAMES[@]} -gt 0 ] && list_contains "$name" "${MISSING_AGENT_NAMES[@]}"; then
    return
  fi

  MISSING_AGENT_NAMES+=("$name")
  MISSING_AGENT_PATHS+=("$path")
  MISSING_AGENT_LOCATIONS+=("$location")
}

scan_deep_claude_plugin_sources() {
  local found_any=false
  local -a plugin_roots=(
    "$HOME/.claude/plugins/marketplaces/claude-plugins-official/plugins"
    "$HOME/.claude/plugins/marketplaces/claude-plugins-official/external_plugins"
    "$HOME/.claude/plugins/cache"
  )
  local -a plugin_labels=(
    "Claude plugin marketplace"
    "Claude external plugins"
    "Claude plugin cache"
  )

  echo -e "\n${BOLD}Deep Claude plugin scan:${RESET}"

  for idx in "${!plugin_roots[@]}"; do
    local root="${plugin_roots[idx]}"
    local label="${plugin_labels[idx]}"

    echo -e "\n${CYAN}${label}${RESET} ($root):"
    if [ ! -d "$root" ]; then
      echo "  (none)"
      continue
    fi

    local found_here=false
    local found_skills_here=false
    local found_agents_here=false

    echo "  Skills:"
    while IFS= read -r skill_file; do
      [ -n "$skill_file" ] || continue
      local skill_dir
      local name
      skill_dir="$(dirname "$skill_file")"
      name="$(basename "$skill_dir")"

      if [ ${#MISSING_SKILL_NAMES[@]} -gt 0 ] && list_contains "$name" "${MISSING_SKILL_NAMES[@]}"; then
        continue
      fi

      echo "    - $name"
      register_missing_skill "$name" "$skill_dir" "$label"
      found_any=true
      found_here=true
      found_skills_here=true
    done < <(find "$root" -type f -name 'SKILL.md' | sort -u)

    if [ "$found_skills_here" = false ]; then
      echo "    (none)"
    fi

    echo "  Agents:"
    while IFS= read -r agent_file; do
      [ -n "$agent_file" ] || continue
      local name
      name="$(basename "$agent_file" .md)"
      [ "$name" = "README" ] && continue

      if [ ${#MISSING_AGENT_NAMES[@]} -gt 0 ] && list_contains "$name" "${MISSING_AGENT_NAMES[@]}"; then
        continue
      fi

      echo "    - $name"
      register_missing_agent "$name" "$agent_file" "$label"
      found_any=true
      found_here=true
      found_agents_here=true
    done < <(find "$root" -type f -path '*/agents/*.md' | sort -u)

    if [ "$found_agents_here" = false ]; then
      echo "    (none)"
    fi

    if [ "$found_here" = false ]; then
      echo "  ${DIM}No additional importable components found here.${RESET}"
    fi
  done

  if [ "$found_any" = false ]; then
    echo -e "\n${DIM}No additional Claude plugin components found to import.${RESET}"
  fi
}

list_installed_components() {
  local -a location_names=(
    "Claude Code current repo install"
    "Claude Code home directory install"
    "Codex current repo install"
    "Codex home directory install"
  )
  local -a location_paths=(
    "$SCRIPT_DIR/.claude"
    "$HOME/.claude"
    "$SCRIPT_DIR/.codex"
    "$HOME/.codex"
  )

  echo -e "\n${BOLD}Installed components by location:${RESET}"

  MISSING_SKILL_NAMES=()
  MISSING_SKILL_PATHS=()
  MISSING_SKILL_LOCATIONS=()
  MISSING_AGENT_NAMES=()
  MISSING_AGENT_PATHS=()
  MISSING_AGENT_LOCATIONS=()

  for idx in "${!location_paths[@]}"; do
    local label="${location_names[idx]}"
    local base="${location_paths[idx]}"
    local skills_dir="$base/skills"
    local agents_dir="$base/agents"
    local agent_ext="md"

    case "$base" in
      */.codex)
        agent_ext="toml"
        ;;
    esac

    echo -e "\n${CYAN}${label}${RESET}"
    echo "  Skills ($skills_dir):"

    if [ ! -d "$skills_dir" ]; then
      echo "    (none)"
    else
      local found_skills=false
      for skill_path in "$skills_dir"/*; do
        [ -d "$skill_path" ] || continue
        [ -f "$skill_path/SKILL.md" ] || continue
        local name
        name="$(basename "$skill_path")"
        echo "    - $name"
        found_skills=true
        register_missing_skill "$name" "$skill_path" "$label"
      done

      if [ "$found_skills" = false ]; then
        echo "    (none)"
      fi
    fi

    echo "  Agents ($agents_dir):"
    if [ ! -d "$agents_dir" ]; then
      echo "    (none)"
      continue
    fi

    local found_agents=false
    for agent_path in "$agents_dir"/*; do
      [ -f "$agent_path" ] || continue
      case "$agent_path" in
        *."$agent_ext")
          local agent_name
          agent_name="$(basename "$agent_path" ."$agent_ext")"
          [ "$agent_name" = "README" ] && continue
          echo "    - $agent_name"
          found_agents=true
          register_missing_agent "$agent_name" "$agent_path" "$label"
          ;;
      esac
    done

    if [ "$found_agents" = false ]; then
      echo "    (none)"
    fi
  done

  if [ "$DEEP_SCAN" -eq 1 ]; then
    scan_deep_claude_plugin_sources
  elif [ -t 0 ]; then
    read -rp "Run deep scan for Claude plugin skills and agents too? (y/N) " scan_plugins_reply
    if [[ "$scan_plugins_reply" =~ ^[Yy]$ ]]; then
      scan_deep_claude_plugin_sources
    fi
  fi

  if [ ${#MISSING_SKILL_NAMES[@]} -gt 0 ]; then
    echo -e "\n${YELLOW}Skills installed but missing from ${SKILLS_SRC}:${RESET}"
    for i in "${!MISSING_SKILL_NAMES[@]}"; do
      echo -e "  ${MISSING_SKILL_LOCATIONS[i]}: ${MISSING_SKILL_NAMES[i]}"
    done

    if [ -t 0 ]; then
      read -rp "Copy these skills into source? (y/N) " reply
      if [[ "$reply" =~ ^[Yy]$ ]]; then
        for i in "${!MISSING_SKILL_NAMES[@]}"; do
          copy_skill_into_repo "${MISSING_SKILL_PATHS[i]}" "${MISSING_SKILL_NAMES[i]}"
        done
      else
        echo "Skipping copy."
      fi
    fi
  else
    echo -e "\n${GREEN}All installed skills already appear in ${SKILLS_SRC}.${RESET}"
  fi

  if [ ${#MISSING_AGENT_NAMES[@]} -gt 0 ]; then
    echo -e "\n${YELLOW}Agents installed but missing from ${AGENTS_SRC}:${RESET}"
    for i in "${!MISSING_AGENT_NAMES[@]}"; do
      echo -e "  ${MISSING_AGENT_LOCATIONS[i]}: ${MISSING_AGENT_NAMES[i]}"
    done

    if [ -t 0 ]; then
      read -rp "Copy these agents into source? (y/N) " reply
      if [[ "$reply" =~ ^[Yy]$ ]]; then
        for i in "${!MISSING_AGENT_NAMES[@]}"; do
          copy_agent_into_repo "${MISSING_AGENT_PATHS[i]}" "${MISSING_AGENT_NAMES[i]}"
        done
      else
        echo "Skipping copy."
      fi
    fi
  else
    echo -e "\n${GREEN}All installed agents already appear in ${AGENTS_SRC}.${RESET}"
  fi
}

# ── Interactive menu ───────────────────────────────────────────────────────────

interactive_menu() {
  ensure_install_target
  local skills agents
  read -ra skills <<< "$(discover_skills)"
  read -ra agents <<< "$(discover_agents)"

  local component_choice=""
  while true; do
    echo -e "\n${BOLD}AmazingGenAITools Installer for ${TOOL_LABEL}${RESET}\n"
    echo "What do you want to install?"
    echo "  1) Skills"
    echo "  2) Agents"
    echo "  3) All"
    read -rp "Choice [1/2/3, default 3]: " component_choice
    case "$component_choice" in
      1|skills)
        component_choice="skills"
        break
        ;;
      2|agents)
        component_choice="agents"
        break
        ;;
      ""|3|all)
        component_choice="all"
        break
        ;;
      *)
        echo -e "${YELLOW}Please enter 1, 2, or 3.${RESET}"
        ;;
    esac
  done

  local all_items=()
  local all_types=()
  local all_names=()

  if [ "$component_choice" = "skills" ] || [ "$component_choice" = "all" ]; then
    for s in "${skills[@]}"; do
      all_items+=("skill:$s")
      all_types+=("skill")
      all_names+=("$s")
    done
  fi

  if [ "$component_choice" = "agents" ] || [ "$component_choice" = "all" ]; then
    for a in "${agents[@]}"; do
      all_items+=("agent:$a")
      all_types+=("agent")
      all_names+=("$a")
    done
  fi

  local total=${#all_items[@]}
  if [ "$total" -eq 0 ]; then
    echo -e "${RED}No installable components found for ${TOOL_LABEL}.${RESET}"
    exit 1
  fi

  echo -e "Select components to install (space-separated numbers, ${BOLD}a${RESET} for all, ${BOLD}q${RESET} to quit):\n"

  local i=1
  if [ "$component_choice" = "skills" ] || [ "$component_choice" = "all" ]; then
    echo -e "${CYAN}  Skills:${RESET}"
    for s in "${skills[@]}"; do
      local marker=" "
      [ -L "$SKILLS_DST/$s" ] && marker="${GREEN}*${RESET}"
      printf "  ${BOLD}%2d${RESET}) %b %-30s\n" "$i" "$marker" "$s"
      ((i++))
    done
  fi

  if [ "$component_choice" = "all" ]; then
    echo -e "\n${CYAN}  Agents:${RESET}"
  elif [ "$component_choice" = "agents" ]; then
    echo -e "${CYAN}  Agents:${RESET}"
  fi

  if [ "$component_choice" = "agents" ] || [ "$component_choice" = "all" ]; then
    for a in "${agents[@]}"; do
      local marker=" "
      [ -e "$AGENTS_DST/${a}.${AGENT_EXT}" ] && marker="${GREEN}*${RESET}"
      printf "  ${BOLD}%2d${RESET}) %b %-30s\n" "$i" "$marker" "$a"
      ((i++))
    done
  fi

  echo -e "\n  ${DIM}(${GREEN}*${RESET}${DIM} = already installed)${RESET}\n"

  read -rp "Choice: " choice

  if [ "$choice" = "q" ] || [ "$choice" = "Q" ]; then
    echo "Cancelled."
    exit 0
  fi

  local selections=()
  if [ "$choice" = "a" ] || [ "$choice" = "A" ]; then
    for ((j=0; j<total; j++)); do
      selections+=("$j")
    done
  else
    for num in $choice; do
      if [[ "$num" =~ ^[0-9]+$ ]] && [ "$num" -ge 1 ] && [ "$num" -le "$total" ]; then
        selections+=("$((num - 1))")
      else
        echo -e "${RED}Invalid selection: $num${RESET}"
      fi
    done
  fi

  if [ ${#selections[@]} -eq 0 ]; then
    echo "Nothing selected."
    exit 0
  fi

  echo ""
  for idx in "${selections[@]}"; do
    local type="${all_types[$idx]}"
    local name="${all_names[$idx]}"
    if [ "$type" = "skill" ]; then
      install_skill "$name"
    else
      install_agent "$name"
    fi
  done
  echo -e "\n${GREEN}Done.${RESET} Restart ${TOOL_LABEL} to pick up new components.\n"
}

# ── CLI dispatch ───────────────────────────────────────────────────────────────

install_all_skills() {
  local skills
  read -ra skills <<< "$(discover_skills)"
  echo -e "\n${BOLD}Installing all skills...${RESET}"
  for s in "${skills[@]}"; do install_skill "$s"; done
  echo ""
}

install_all_agents() {
  if [ "$SUPPORTS_AGENTS" -ne 1 ]; then
    echo -e "\n${YELLOW}Skipping agents for ${TOOL_LABEL}.${RESET}\n"
    return
  fi

  local agents
  read -ra agents <<< "$(discover_agents)"
  echo -e "\n${BOLD}Installing all agents...${RESET}"
  for a in "${agents[@]}"; do install_agent "$a"; done
  echo ""
}

install_by_name() {
  local skills agents
  read -ra skills <<< "$(discover_skills)"
  read -ra agents <<< "$(discover_agents)"

  for name in "$@"; do
    local found=false
    for s in "${skills[@]}"; do
      if [ "$s" = "$name" ]; then
        install_skill "$name"
        found=true
        break
      fi
    done
    if [ "$found" = false ]; then
      for a in "${agents[@]}"; do
        if [ "$a" = "$name" ]; then
          install_agent "$name"
          found=true
          break
        fi
      done
    fi
    if [ "$found" = false ]; then
      echo -e "  ${RED}x${RESET} ${BOLD}$name${RESET} not found in skills or agents"
    fi
  done
}

# ── Main ───────────────────────────────────────────────────────────────────────

main() {
  local tool_option=""
  local -a positionals=()

  while [ $# -gt 0 ]; do
    case "$1" in
      --tool)
        if [ $# -lt 2 ]; then
          echo -e "${RED}Missing value for --tool${RESET}"
          exit 1
        fi
        tool_option="$2"
        shift 2
        ;;
      --tool=*)
        tool_option="${1#*=}"
        shift
        ;;
      --deep)
        DEEP_SCAN=1
        shift
        ;;
      *)
        positionals+=("$1")
        shift
        ;;
    esac
  done

  if [ -n "$tool_option" ]; then
    configure_tool "$tool_option"
  fi

  if [ ${#positionals[@]} -gt 0 ]; then
    set -- "${positionals[@]}"
  else
    set --
  fi

  if [ $# -eq 0 ]; then
    interactive_menu
    exit 0
  fi

  case "$1" in
    --all|-a)
      install_all_skills
      install_all_agents
      echo -e "${GREEN}All components installed.${RESET} Restart ${TOOL_LABEL} to pick up new components.\n"
      ;;
    --skills|-s)
      install_all_skills
      ;;
    --agents|-g)
      install_all_agents
      ;;
    --list|-l)
      list_components
      ;;
    --installed|-i)
      list_installed_components
      ;;
    --help|-h)
      echo -e "\n${BOLD}Usage:${RESET} ./install.sh [OPTIONS] [NAMES...]"
      echo ""
      echo "  ${BOLD}(no args)${RESET}        Interactive selection menu"
      echo "  ${BOLD}--tool <name>${RESET}      Select target tool: claude or codex"
      echo "  ${BOLD}--all,  -a${RESET}       Install all skills and agents"
      echo "  ${BOLD}--skills, -s${RESET}     Install all skills"
      echo "  ${BOLD}--agents, -g${RESET}     Install all agents"
      echo "  ${BOLD}--list, -l${RESET}       List available components and install status"
      echo "  ${BOLD}--installed, -i${RESET}  Show currently installed skills (home + repo) and import missing ones"
      echo "  ${BOLD}--deep${RESET}             With --installed, also scan Claude plugin sources for skills and agents"
      echo "  ${BOLD}<name> ...${RESET}       Install specific items by name"
      echo ""
      echo "Environment:"
      echo "  AI_INSTALL_TARGET=repo|home    Select install destination"
      echo ""
      echo "Examples:"
      echo "  ./install.sh                         # Interactive menu"
      echo "  ./install.sh --all                   # Install everything"
      echo "  ./install.sh --tool codex --skills   # Install all skills for Codex"
      echo "  ./install.sh --installed --deep"
      echo "  ./install.sh learn-process           # Install one skill"
      echo "  ./install.sh learn-sync learning-orchestrator  # Install specific items"
      echo ""
      ;;
    --*)
      echo -e "${RED}Unknown option: $1${RESET}"
      echo "Run ./install.sh --help for usage."
      exit 1
      ;;
    *)
      install_by_name "$@"
      ;;
  esac
}

main "$@"
