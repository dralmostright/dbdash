import { MountItem } from "./MountItem";

export function MountList({
    mounts,
    setMounts,
    mountInputs,
    handleMountChange,
    deleteMountFromRepo
}) {
    const removeMountLocal = (index) => {
        setMounts((prev) => prev.filter((_, i) => i !== index));
    };

    return (
        <>
            {mounts.map((mount, index) => (
                <MountItem
                    key={mount.msdbsm_id || index}
                    mount={mount}
                    index={index}
                    mountInputs={mountInputs}
                    onChange={handleMountChange}
                    onRemove={removeMountLocal}
                    onDeleteFromRepo={deleteMountFromRepo}
                    canRemove={mounts.length > 1}
                />
            ))}
        </>
    );
}
