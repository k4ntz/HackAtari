#!/bin/bash

#Boxing_Opt=("gravity" "-db" "one_armed")
BankHeist_Opt=("unlimited_gas" "no_police" "only_police" "random_city" "revisit_city")
BattleZone_Opt=("no_radar")
Boxing_Opt=("gravity1" "gravity3" "gravity5" "one_armed" "drunken_boxing" "color_p0" "color_p4")
Breakout_Opt=("strength1" "strength3" "driftr" "driftl" "gravity" "inverse_gravity" "color_p0" "color_p4" "color_b0" "color_b4" "color_r14" "color_r24")
Carnival_Opt=("no_flying_ducks" "unlimited_ammo" "fast_missiles1" "fast_missiles2" "fast_missiles3")
ChopperCommand_Opt=("delay_shots" "no_enemies" "no_radar" "invis_player" "color0" "color2" "color4")
DonkeyKong_Opt=("no_barrel" "random_start")
FishingDerby_Opt=("fish_mode0" "fish_mode1" "fish_mode3" "shark_mode0" "shark_mode1" "shark_mode2" "shark_mode3")
Freeway_Opt=("stop1" "stop2" "stop3" "color1" "color3" "color5" "color8")
Frostbite_Opt=("color0" "color3" "line1" "line2" "line3" "line4" "line5" "enemies0" "enemies3")
Kangaroo_Opt=("disable_monkeys" "disable_coconut" "random_init" "set_floor0" "set_floor2" "change_level0" "change_level2")
MontezumaRevenge_Opt=("random_position_start" "level0" "level3" "level6" "level9" "randomize_items" "full_inventory")
MsPacman_Opt=("caged_ghosts" "disable_orange" "disable_red" "disable_cyan" "disable_pink" "power0" "power4" "edible_ghosts" "inverted" "change_level0" "change_level3")
Pong_Opt=("lazy_enemy" "up_drift1" "up_drift5" "down_drift1" "down_drift5" "left_drift1" "left_drift5" "right_drift1" "right_drift5")
RiverRaid_Opt=("no_fuel")
Seaquest_Opt=("unlimited_oxygen" "gravity" "disable_enemies" "random_color_enemies")
Skiing_Opt=("invert_flags")
SpaceInvaders_Opt=("disable_shield_left" "disable_shield_middle" "disable_shield_right" "disable_shields" "curved")
Tennis_Opt=("wind" "upper_pitches" "lower_pitches" "upper_player" "lower_player")

check_dialog_installed() {
    # Check if dialog is installed
    if ! command -v dialog &> /dev/null; then
    	show_infobox "dialog is not installed. Please install it and try again."
        echo "dialog is not installed. Please install it and try again."
        exit 1
    fi
}

show_infobox() {
    local text="$1"
    dialog --clear --title "Info" --msgbox "$text" 10 40
    clear
    return 1
}

run_game() {
    sel_game="$1"
    sel_model="$2"
    # show_infobox "$sel_game"
    if [ "$sel_model" = "Human" ]; then
    	clear
        if [ "$choosen_options" == "" ]; then
            # show_infobox "python run.py -g "$sel_game" -hu"
            python3 run.py -g "$sel_game" -hu
            exit 1
        else
            # show_infobox "python run.py -g "$sel_game" -hu -m $choosen_options"
            python3 run.py -g "$sel_game" -hu -m $choosen_options
        fi
        # python run.py -g "$sel_game" -hu "$choosen_options"
        # show_infobox "python run.py -g "$sel_game" -hu "${choosen_options[*]}""
    else
    	clear
    	if [ "$choosen_options" == "" ]; then
    	    # show_infobox "python run.py -g $sel_game -a models/$sel_game/$sel_model"
            python3 run.py -g "$sel_game" -a models/$sel_game/$sel_model
        else
            # show_infobox "python run.py -g $sel_game -a models/$sel_game/$sel_model -m $choosen_options"
            python3 run.py -g "$sel_game" -a models/$sel_game/$sel_model -m $choosen_options
        fi
        # python run.py -g "$sel_game" $model "$choosen_options" "${choosen_options[@]}"
        #show_infobox "python run.py -g "$sel_game" $sel_model "${choosen_options[*]}""
        # exit 1
    fi
}

game_menu() {
    # Create an array to store the menu options
    local menu_options=()
    local i=1
    # Populate the Menu with the Games
    declare -a games=("BankHeist" "BattleZone" "Boxing" "Breakout" "Carnival" "ChopperCommand" "DonkeyKong" "FishingDerby" "Freeway" "Frostbite" "Kangaroo" "MontezumaRevenge" "MsPacman" "Pong" "RiverRaid" "Seaquest" "Skiing" "SpaceInvaders" "Tennis")

    #show_infobox "${#games[@]}"
    length=${#games[@]}
    pos=$((length+1))
    for ((j=0; j<${length}; j++ )); do
        #show_infobox "$j"
        #show_infobox "${games[$j]}"
        menu_options+=("$((j+1))" ${games[$j]})
    done
    menu_options+=("$pos" "System")
    sys_pos=$pos
    ((pos+=1))
    #menu_options+=("$pos" "Reboot")
    #reboot_pos=$pos
    #((pos+=1))
    #menu_options+=("$pos" "Shutdown")
    #shutdown_pos=$pos

    # Check if there are any menu_options to display
    if [ ${#menu_options[@]} -eq 0 ]; then
        # show_infobox "No Options!."
        exit 1
    fi
    
    while true; do
    GAME=$(dialog --clear \
                  --backtitle "Game Launcher" \
                  --title "Select a Game" \
                  --no-ok --no-cancel \
                  --menu "Choose a game:" \
                  18 50 4 \
                  "${menu_options[@]}" \
                  2>&1 >/dev/tty)

    # Clear the screen after dialog
    # show_infobox "reboot: $reboot_pos. choosen: $GAME"
    clear

    #if [[ $reboot_pos -eq $GAME ]]; then
    #    systemctl reboot -i
    #    return 1
    #fi

    #if [[ $shutdown_pos -eq $GAME ]]; then
        # show_infobox "poweroff"
    #    shutdown --no-wall -h 0
    #    return 1
    #fi

    # Run the selected script
    if [[ $sys_pos -eq $GAME ]]; then
            system_menu
    else
        if [ -n "$GAME" ]; then
            local selected="${menu_options[$((GAME * 2 - 1))]}"
            # show_infobox "$selected"
            model_menu "$selected"
        else
            echo "No game selected."
            return 1
        fi
    fi
    done
}

system_menu() {
    # Create an array to store the menu options
    local menu_options=()
    local i=1
    
    menu_options+=("$pos" "Update")
    update_pos=$pos
    ((pos+=1))
    menu_options+=("$pos" "Reboot")
    reboot_pos=$pos
    ((pos+=1))
    menu_options+=("$pos" "Shutdown")
    shutdown_pos=$pos
    ((pos+=1))
    menu_options+=("$pos" "Return")
    ret_pos=$pos
    ((pos+=1))
    
    while true; do
    CHOICE=$(dialog --clear \
                  --backtitle "Game Launcher" \
                  --title "Options" \
                  --no-ok --no-cancel \
                  --menu "Choose:" \
                  18 50 4 \
                  "${menu_options[@]}" \
                  2>&1 >/dev/tty)

    # Clear the screen after dialog
    # show_infobox "reboot: $reboot_pos. choosen: $GAME"
    clear
        if [[ $update_pos -eq $CHOICE ]]; then
        cd ~/arcade/OC_Atari
        git pull origin master
        python setup.py install

        cd ~/arcade/HackAtari
        git pull origin master
        pip3 install -e .

        systemctl reboot -i
        return 1
    fi

    if [[ $ret_pos -eq $CHOICE ]]; then
        return
    fi

    if [[ $reboot_pos -eq $CHOICE ]]; then
        systemctl reboot -i
        return 1
    fi

    if [[ $shutdown_pos -eq $CHOICE ]]; then
        # show_infobox "poweroff"
        shutdown --no-wall -h 0
        return 1
    fi
    done
}

model_menu() {
    choosen_options=""

    local game="$1"
    local dir="models/$(echo $game | tr -d " ")"

    # Check if the directory exists
    #if [ ! -d "$dir" ]; then
    #    show_infobox "Directory $dir does not exist."
    #    return 1
    #fi

    # Create an array to store the menu options
    local menu_options=()
    local i=1

    # Populate the menu options with the files in the directory
    if [ ! -d "$dir" ]; then
        echo "directory does not exist"
        # show_infobox "Directory $dir does not exist."
    else
        for file in "$dir"/*; do
            if [ -f "$file" ]; then
                menu_options+=("$i" "$(basename "$file")")
                ((i++))
            fi
        done
    fi
    menu_options+=("$i" "Human")
    human_pos=$i
    ((i++))
    menu_options+=("$i" "Options")
    options_pos=$i
    ((i++))
    menu_options+=("$i" "Return")
    return_pos=$i

    # Check if there are any files to display
    #if [ ${#menu_options[@]} -eq 0 ]; then
    #    echo "No files found in directory $dir."
    #    exit 1
    #fi

    # Display the dialog menu and get user selection
    while true; do
        local choice
        choice=$(dialog --clear --title "Select a script to run for $game" --no-ok --no-cancel \
                        --menu "Choose one of the following scripts:" 15 50 10 \
                        "${menu_options[@]}" 2>&1 >/dev/tty)

        # Clear the screen after dialog
        clear

        if [[ $options_pos -eq $choice ]]; then
            options_menu "$game"
        else
            if [[ $return_pos -eq $choice ]]; then
                return 1
            else
                # Run the selected script
                if [ -n "$choice" ]; then
                    selected_model="${menu_options[$((choice * 2 - 1))]}"
                    run_game "$game" "$selected_model"
                    return 1
                else
                    return 1
                fi
            fi
        fi
    done
}

options_menu() {
    local game="$1"
    local suffix=_Opt
    local varname="${game}${suffix}"
    # eval "options= (\"\${${varname[@]}\"})"    # ${!varname}
    eval "options=(\"\${${varname}[@]}\")"
    #show_infobox $options

    # Create an array to store the checklist options
    local checklist_options=()
    for option in "${options[@]}"; do
        checklist_options+=("$option" "" "off")
    done

    # Display the dialog checklist and get user selections
    local choices
    choices=$(dialog --clear --title "$title" --no-ok --no-cancel \
                     --checklist "Select options:" 15 50 10 \
                     "${checklist_options[@]}" 2>&1 >/dev/tty)

    # Clear the screen after dialog
    clear

    # Return the selected options
    if [ -n "$choices" ]; then
        echo "$choices"
        # show_infobox "Selected options: -- $choices --"
        choosen_options=$choices
        # show_infobox "test $testvar"
    else
        echo ""
        return 1
    fi
}

start() {
    source ~/arcade/venv/bin/activate
    cd ~/arcade/HackAtari
    check_dialog_installed
    game_menu
    #model_menu "Boxing"
    #options_menu "Boxing"
    #suffix=_Opt
    #varname=Test$suffix
    #echo ${!varname}
    #show_infobox "Return!"
}

start