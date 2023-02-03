import { Button } from '@kobalte/core'
import { FaSolidGear } from 'solid-icons/fa'
import WebSocketHandler from '@components/WebSocket'
import { ICamera } from '@src/store/camera/camera'
import { ActiveStatus, CapitalizeFirstLetter } from '@src/utils/utils'
export interface IList extends ICamera {
    onClick: () => void
}

const List = (props: IList) => {
    return (
        <div class="grid grid-flow-col auto-cols-fr pl-[12px] pt-[12px] pb-[12px] rounded-[10px] mb-[20px] bg-[#333742] text-white">
            <div class="flex items-center w-[500px]">
                <div>
                    <div class="text-[#FFFF] bg-[#FFFF] w-[60px] h-[60px] rounded-[5px]">
                        <WebSocketHandler borderRadius="rounded-[5px]" />
                    </div>
                </div>
                <div>
                    <div class="flex items-center justify-center text-left pl-[10px]">
                        <div class="mr-[8px]">
                            <p>{props.address}</p>
                        </div>
                        <Button.Root aria-label="Settings" onClick={() => props.onClick()}>
                            <FaSolidGear size={15} />
                        </Button.Root>
                    </div>
                    <div class="flex items-center">
                        <div class="text-left pl-[10px] pr-[10px]">
                            <p>{CapitalizeFirstLetter(props.status.toLocaleLowerCase())}</p>
                        </div>
                        <div
                            class={'ml-[6px] w-[10px] h-[10px] rounded-[100%]'}
                            style={{ background: ActiveStatus(props.status) }}
                        />
                    </div>
                </div>
            </div>
            <div class="flex items-center justify-center ">
                <p class="text-left w-[150px] m-auto  max-md:text-right">{props.address}</p>
            </div>
            <div class="flex items-center text-left w-[150px] m-auto max-md:hidden">
                <p>{CapitalizeFirstLetter(props.status.toLocaleLowerCase())}</p>
                <div
                    class={'ml-[6px] w-[10px] h-[10px] rounded-[100%]'}
                    style={{ background: ActiveStatus(props.status) }}
                />
            </div>
            <div class="flex items-center justify-center max-sm:hidden">
                <p class="text-left w-[150px] m-auto  max-md:text-right">
                    {CapitalizeFirstLetter(props.type.toLocaleLowerCase())}
                </p>
            </div>
        </div>
    )
}

export default List