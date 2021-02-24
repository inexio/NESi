#!/bin/bash
# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
#
# License: https://github.com/inexio/NESi/LICENSE.rst
#
# Example NESi REST API server bootstrapping
#
ENDPOINT=http://localhost:5000/nesi/v1

path="`dirname \"$0\"`"

. $path/functions.sh

echo "What vendor?"
read vendor
if [ $vendor != "Alcatel" ] && [ $vendor != "Huawei" ]; then
    until [ $vendor == "Alcatel" ] || [ $vendor == "Huawei" ]
    do
        echo "Invalid vendor. Please enter a correct one. (Alcatel, Huawei)"
        read vendor
    done
fi

if [ $vendor == "Alcatel" ] ; then
    echo "What model?"
    read model
    if [ $model != "7360" ] && [ $model != "7330" ] && [ $model != "7356" ] && [ $model != "7363" ]; then
      until [ $model == "7360" ] || [ $model == "7330" ] || [ $model == "7356" ] || [ $model == "7363" ]
      do
          echo "Invalid model. Please enter a correct one. (7360, 7330, 7356, 7363)"
          read model
      done
    fi
    echo "Which version?"
    read version
    if [ $version != "1" ] && [ $version != "FX-4" ] && [ $version != "FX-8" ]; then
        until [ $version == "1" ] || [ $version == "FX-4" ] || [ $version == "FX-8" ]
        do
            echo "Invalid version. Please enter a correct one. (FX-4, FX-8, 1)"
            read version
        done
    fi
fi

if [ $vendor == "Huawei" ] ; then
    echo "What model?"
    read model
    if [ $model != "5603" ] && [ $model != "5606" ] && [ $model != "5608" ] && [ $model != "5616" ] && [ $model != "5622" ] && [ $model != "5623" ]; then
      until [ $model == "5603" ] || [ $model == "5606" ] || [ $model == "5608" ] || [ $model == "5616" ] || [ $model == "5622" ] || [ $model == "5623" ]
      do
          echo "Invalid model. Please enter a correct one. (5603, 5606, 5608, 5616, 5622, 5623)"
          read model
      done
    fi
    echo "Which version?"
    read version
    if [ $version != "1" ] && [ $version != "A" ] && [ $version != "T" ]; then
        until [ $version == "1" ] || [ $version == "A" ] || [ $version == "T" ]
        do
            echo "Invalid version. Please enter a correct one. (A, T, 1)"
            read version
        done
    fi
fi

echo "How many subracks?"
read subrack_count

req_file=$(mktemp /tmp/requirements.txt)

echo '{
    "vendor": "'$vendor'",
    "model": "'$model'",
    "version": "'$version'",
    "description": "Custom Benchmark Switch",
    "hostname": "Custom_Benchmark",
    "mgmt_address": "10.0.0.13",
    "network_protocol": "telnet",
    "network_address": "127.0.0.1",
    "network_port": 9023,
    "software_version": "Benchmark 2.0",
    "credentials": {
        "1": {
            "username": "admin",
            "password": "secret"
        }
    },
    ' >> $req_file

i=1
subracks_file=$(mktemp /tmp/subracks.txt)
echo '    "subracks": {' >> $subracks_file

cards_file=$(mktemp /tmp/cards.txt)
echo '    "cards": {' >> $cards_file

ports_file=$(mktemp /tmp/ports.txt)
echo '    "ports": {' >> $ports_file

onts_file=$(mktemp /tmp/onts.txt)
echo '    "onts": {' >> $onts_file

ont_ports_file=$(mktemp /tmp/ont_ports.txt)
echo '    "ont_ports": {' >> $ont_ports_file

cpes_file=$(mktemp /tmp/cpes.txt)
echo '    "cpes": {' >> $cpes_file

cpe_ports_file=$(mktemp /tmp/cpe_ports.txt)
echo '    "cpe_ports": {' >> $cpe_ports_file

total_subrack_count=1
total_port_count=1
total_card_count=1
total_ont_count=1
total_ont_port_count=1
total_cpe_count=1
total_cpe_port_count=1
until [ $i -gt $subrack_count ]
do
    echo 'Creating subrack '$i'/'$subrack_count
    echo "How many cards on subrack $i?"
    read card_count
    j=1
    until [ $j -gt $card_count ]
    do
        echo 'Creating card '$j'/'$card_count
        echo 'What card type on card '$j'? (xdsl, vdsl, adsl, sdsl, ftth, ftth-pon)'
        read card_type
        if [ $card_type == "ftth" ] && [ $vendor == "Huawei" ]; then
            echo "H802OPGE or H831EIUD?"
            read board_name
            if [ $board_name != "H802OPGE" ] && [ $board_name != "H831EIUD" ]; then
                until [ $board_name == "H802OPGE" ] || [ $board_name == "H831EIUD" ]
                do
                    echo "Invalid input, please try again. (H802OPGE or H831EIUD?)"
                    read board_name
                done
            fi
        fi
        echo "How many ports on card $j?"
        read port_count
        if [ $card_type == 'ftth-pon' ]; then
            echo "How many onts per port?"
            read ont_count
        fi
        k=1
        if [ $port_count -le 64 ] && [ $port_count -ge 48 ]; then
            ppc=64
        elif [ $port_count -le 48 ] && [ $port_count -ge 32 ]; then
            ppc=48
        elif [ $port_count -le 32 ] && [ $port_count -ge 16 ]; then
            ppc=32
        elif [ $port_count -le 16 ] && [ $port_count -ge 8 ]; then
            ppc=16
        elif [ $port_count -le 8 ]; then
            ppc=8
        fi
        until [ $k -gt $port_count ]
        do
            echo 'Creating port '$k'/'$port_count
            if [ $vendor == "Alcatel" ]; then
              name="1/$i/$j/$k"
              admin="up"
            elif [ $vendor == "Huawei" ]; then
              name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`"
              admin="activated"
            fi
            echo '        "'$total_port_count'": {
            "name": "'$name'",
            "description": "Physical port #'$k'",
            "card_id": '$total_card_count',
            "operational_state": "1",
            "admin_state": "'$admin'"
        },' >> $ports_file

            case $card_type in
                ftth-pon)
                    l=1
                    until [ $l -gt $ont_count ]
                    do
                        if [ $vendor == "Alcatel" ]; then
                          name="1/$i/$j/$k/$l"
                        elif [ $vendor == "Huawei" ]; then
                          name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/`expr $l - 1`"
                        fi
                        echo '        "'$total_ont_count'": {
            "name": "'$name'",
            "description": "Physical ont #'$l'",
            "index": '$l',
            "port_id": '$total_port_count'
        },' >> $onts_file
                        for p in 1 2 3 4
                        do
                            if [ $vendor == "Alcatel" ]; then
                              name="1/$i/$j/$k/$l/1/$p"
                            elif [ $vendor == "Huawei" ]; then
                              name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/`expr $l - 1`/$p"
                            fi
                            echo '        "'$total_ont_port_count'": {
            "name": "'$name'",
            "description": "Physical ont_port #'$p'",
            "ont_id": '$total_ont_count'
        },' >> $ont_ports_file
                            if [ $vendor == "Alcatel" ]; then
                              name="1/$i/$j/$k/$l/1/$p/1"
                            elif [ $vendor == "Huawei" ]; then
                              name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/`expr $l - 1`/$p/1"
                            fi
                            echo '        "'$total_cpe_count'": {
            "name": "'$name'",
            "description": "Physical cpe #1",
            "ont_port_id": '$total_ont_port_count'
        },' >> $cpes_file
                              for q in 1 2 3 4
                              do
                                  if [ $vendor == "Alcatel" ]; then
                                    name="1/$i/$j/$k/$l/1/$p/1/$q"
                                  elif [ $vendor == "Huawei" ]; then
                                    name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/`expr $l - 1`/$p/1/$q"
                                  fi
                                  echo '        "'$total_cpe_port_count'": {
            "name": "'$name'",
            "description": "Physical cpe_port #'$q'",
            "cpe_id": '$total_cpe_count'
        },' >> $cpe_ports_file
                                  ((total_cpe_port_count++))
                              done
                              ((total_cpe_count++))

                            ((total_ont_port_count++))
                        done
                    ((l++))
                    ((total_ont_count++))
                    done
                       ;;
                ftth)
                    if [ $vendor == "Alcatel" ]; then
                      name="1/$i/$j/$k/1"
                    elif [ $vendor == "Huawei" ]; then
                      name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/0"
                    fi
                    echo '        "'$total_ont_count'": {
            "name": "'$name'",
            "description": "Physical ont #1",
            "index": 1,
            "port_id": '$total_port_count'
        },' >> $onts_file
                    for n in 1 2 3 4
                    do
                        if [ $vendor == "Alcatel" ]; then
                          name="1/$i/$j/$k/1/1/$n"
                        elif [ $vendor == "Huawei" ]; then
                          name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/0/$n"
                        fi
                        echo '        "'$total_ont_port_count'": {
            "name": "'$name'",
            "description": "Physical ont_port #'$n'",
            "ont_id": '$total_ont_count'
        },' >> $ont_ports_file
                        if [ $vendor == "Alcatel" ]; then
                          name="1/$i/$j/$k/1/1/$n/1"
                        elif [ $vendor == "Huawei" ]; then
                          name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/0/$n/1"
                        fi
                        echo '        "'$total_cpe_count'": {
            "name": "'$name'",
            "description": "Physical cpe #1",
            "ont_port_id": '$total_ont_port_count'
        },' >> $cpes_file
                          for o in 1 2 3 4
                          do
                              if [ $vendor == "Alcatel" ]; then
                                name="1/$i/$j/$k/1/1/$n/1/$0"
                              elif [ $vendor == "Huawei" ]; then
                                name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/0/$n/1/$o"
                              fi
                              echo '        "'$total_cpe_port_count'": {
            "name": "'$name'",
            "description": "Physical cpe_port #'$o'",
            "cpe_id": '$total_cpe_count'
        },' >> $cpe_ports_file
                              ((total_cpe_port_count++))
                          done
                          ((total_cpe_count++))

                        ((total_ont_port_count++))
                    done
                    ((total_ont_count++))
                       ;;
                xdsl | vdsl | adsl | sdsl)
                    if [ $vendor == "Alcatel" ]; then
                      name="1/$i/$j/$k/1"
                    elif [ $vendor == "Huawei" ]; then
                      name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/1aa"
                    fi
                    echo '        "'$total_cpe_count'": {
            "name": "'$name'",
            "description": "Physical cpe #1",
            "port_id": '$total_port_count'
        },' >> $cpes_file
                    for m in 1 2 3 4
                    do
                        if [ $vendor == "Alcatel" ]; then
                          name="1/$i/$j/$k/1/$m"
                        elif [ $vendor == "Huawei" ]; then
                          name="`expr $i - 1`/`expr $j - 1`/`expr $k - 1`/0/$m"
                        fi
                        echo '        "'$total_cpe_port_count'": {
            "name": "'$name'",
            "description": "Physical cpe_port #'$m'",
            "cpe_id": '$total_cpe_count'
        },' >> $cpe_ports_file
                        ((total_cpe_port_count++))
                    done
                    ((total_cpe_count++))
                       ;;
            esac

            ((k++))
            ((total_port_count++))
        done
        if [ $vendor == "Alcatel" ]; then
          echo '        "'$total_card_count'": {
            "name": "1/'$i'/'$j'",
            "description": "Physical card #'$j'",
            "subrack_id": '$total_subrack_count',
            "operational_state": "1",
            "admin_state": "1",
            "product": "'$card_type'",
            "ppc": "'$ppc'"
        },' >> $cards_file
        elif [ $vendor == "Huawei" ]; then
          name="`expr $i - 1`/`expr $j - 1`"
          echo '        "'$total_card_count'": {
            "name": "'`expr $i - 1`'/'`expr $j - 1`'",
            "description": "Physical card #'$j'",
            "subrack_id": '$total_subrack_count',
            "operational_state": "1",
            "admin_state": "1",
            "product": "'$card_type'",
            "ppc": "'$ppc'",
            "board_name": "'$board_name'"
        },' >> $cards_file
        fi
        ((j++))
        ((total_card_count++))
    done
    if [ $vendor == "Alcatel" ]; then
      name="1/$i"
    elif [ $vendor == "Huawei" ]; then
      name=`expr $i - 1`
    fi
    echo '        "'$i'": {
              "name": "'$name'",
              "description": "Physical subrack #'$i'",
              "operational_state": "1",
              "admin_state": "1"
          },' >> $subracks_file
    ((i++))
    ((total_subrack_count++))
done

sed -i '' '$ s/.$//' $cpe_ports_file
echo "
    }," >> $cpe_ports_file

sed -i '' '$ s/.$//' $cpes_file
echo "
    }," >> $cpes_file

sed -i '' '$ s/.$//' $ont_ports_file
echo "
    }," >> $ont_ports_file

sed -i '' '$ s/.$//' $onts_file
echo "
    }," >> $onts_file

sed -i '' '$ s/.$//' $ports_file
echo "
    }," >> $ports_file

sed -i '' '$ s/.$//' $cards_file
echo "
    }," >> $cards_file

sed -i '' '$ s/.$//' $subracks_file
echo "
    }" >> $subracks_file

cat "$cards_file" >> "$req_file"
rm ${cards_file}

cat "$ports_file" >> "$req_file"
rm ${ports_file}

cat "$cpes_file" >> "$req_file"
rm ${cpes_file}

cat "$cpe_ports_file" >> "$req_file"
rm ${cpe_ports_file}

if [ $total_ont_count -gt 1 ]; then
    cat "$onts_file" >> "$req_file"
fi
rm ${onts_file}

if [ $total_ont_count -gt 1 ]; then
    cat "$ont_ports_file" >> "$req_file"
fi
rm ${ont_ports_file}

cat "$subracks_file" >> "$req_file"
rm ${subracks_file}

echo "
}" >> $req_file

curl -s -d @$req_file -H "Content-Type: application/json" -X POST "127.0.0.1:5000/nesi/v1/boxen"

rm ${req_file}