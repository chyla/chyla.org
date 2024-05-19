OpenWRT Low Throughput
======================

Zmiana parametrów **offloading** pomaga zwiększyć przepustowość,
przynajmniej na **TP-Link Archer A7 AC1750 (hw ver 5)**.

.. code-block:: text

    # for software offload
    uci set firewall.@defaults[0].flow_offloading='1'

    # for hardware offload
    uci set firewall.@defaults[0].flow_offloading_hw='1'

    # save settings
    uci commit

    # restart firewall to apply these settings
    /etc/init.d/firewall restart

Można również spróbować poniższych:

- zmienić **MTU** (maximum transmission unit) interfejsów na większe,
- zmienić **nice** procesu **hostapd** (np. na *-20*),
- wyłączyć IPv6 lub IPv4 i używać tylko jednego z nich,
- zaktualizować OpenWRT (problem jest mniej widoczny na 23.05, niż na 22.*),
- po ustawieniu offload, co jakiś czas pomaga restart usługi firewall: `/etc/init.d/firewall restart`.

Na OpenWRT 23.05, z wflow_offloading=1, MTU=4000, nice=-20, wyłączonym IPv6,
testując jednym klientem, blisko routera udaje się osiągnąć lekko ponad 280Mbps.


Źródła
------

1. `New OpenWrt installation on a TP-Link Archer C7 v2 is slow - speed cut in half <https://forum.openwrt.org/t/new-openwrt-installation-on-a-tp-link-archer-c7-v2-is-slow-speed-cut-in-half/157300>`__
2. `OpenWrt software offloading configuration <https://forum.openwrt.org/t/openwrt-software-offloading-configuration/151081>`__
